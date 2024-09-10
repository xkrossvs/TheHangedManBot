import asyncio
import logging
import sys
import pymongo
from pymongo.collection import Collection
from config import TOKEN, MONGO_URL
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from keyboards import Keyboards
from strings import Strings
from words import words
from random import choice
from hangs import stages
from aiogram.fsm.storage.mongo import MongoStorage
from aiogram.fsm.context import FSMContext
from units import find_all_indices, is_it_a_win
from stickers import win_stickers

storage = MongoStorage.from_url(url=MONGO_URL, db_name='the_hanged_man')
dp = Dispatcher(storage=storage)
cluster = pymongo.MongoClient(MONGO_URL)
users: Collection = cluster.the_hanged_man.users


class GameProcess(StatesGroup):
    game = State()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(text=f"Привет, {message.from_user.full_name}, и добро пожаловать в игру '<b>Висельница</b>'. "
                              f"Нажмите 'Начать игру', чтобы начать игру.",
                         reply_markup=Keyboards.main_menu())
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    if not users.find_one({'user_id': user_id}):
        users.insert_one({'user_id': user_id, 'full_name': full_name,
                          'wins': 0, 'losses': 0, 'WL': 0,
                          'win_streak': 0, 'max_win_streak': 0, 'used_words': []})


@dp.message(F.text == Strings.PROFILE_BUTTON)
async def profile_handler(message: Message):
    user_id = message.from_user.id
    info = users.find_one({'user_id': user_id})
    await message.answer(text=f'Имя: {info['full_name']}\n'
                              f'Количество побед: {info['wins']}\n'
                              f'Количество поражений: {info['losses']}\n'
                              f'Победы/Поражения: {info['WL']}\n'
                              f'Текущая серия побед: {info['win_streak']}\n'
                              f'Максимальная серия побед: {info['max_win_streak']}',
                         reply_markup=Keyboards.main_menu())


@dp.message(F.text == Strings.START_GAME_BUTTON)
async def start_game_handler(message: Message, state: FSMContext, bot: Bot) -> None:
    loading_message = await message.answer(text='Загрузка...',
                                           reply_markup=ReplyKeyboardRemove())
    await bot.delete_message(chat_id=loading_message.chat.id,
                             message_id=loading_message.message_id)
    user_id = message.from_user.id
    used_words = users.find_one({'user_id': user_id})['used_words']
    word = choice(words)
    while word in used_words:
        word = choice(words)
    await state.update_data(word=word)
    text_word = ['_'] * len(word)
    await state.update_data(text_word=text_word)
    hang_state = -1
    await state.update_data(hang_state=hang_state)
    wrong_letters = []
    await state.update_data(wrong_letters=wrong_letters)
    answer = await message.answer(text=f'Загадано слово из {len(word)} букв.\n'
                                       f'У вас есть право на 5 ошибок.\n\n'
                                       f'{' '.join(text_word)}\n'
                                       f'{stages[hang_state]}')
    users.update_one(filter={'user_id': user_id},
                     update={'$push': {'used_words': word}})
    chat_id = answer.chat.id
    await state.update_data(chat_id=chat_id)
    message_id = answer.message_id
    await state.update_data(message_id=message_id)
    await state.set_state(GameProcess.game)


@dp.message(F.text.len() == 1, F.text.upper().in_(Strings.CYRILLIC_LETTERS), GameProcess.game)
async def letter_catcher(message: Message, state: FSMContext, bot: Bot):
    await message.delete()
    user_id = message.from_user.id
    letter = message.text.upper()
    data = await state.get_data()
    word = data['word']
    chat_id = data['chat_id']
    message_id = data['message_id']
    text_word = data['text_word']
    hang_state = data['hang_state']
    wrong_letters = data['wrong_letters']

    if letter not in word:
        if letter in wrong_letters:
            await message.delete()
            return
        wrong_letters.append(letter)
        await state.update_data(wrong_letters=wrong_letters)
        hang_state -= 1
        await state.update_data(hang_state=hang_state)
        if hang_state != -7:
            await bot.edit_message_text(text=f'Вы не отгадали букву.\n'
                                             f'Сожалею, вы на 1 шаг ближе к поражению.\n\n'
                                             f'Осталось прав на ошибку: {6 + hang_state}\n\n'
                                             f'{' '.join(text_word)}\n\n'
                                             f'{stages[hang_state]}\n\n'
                                             f'Неправильные буквы: {' '.join(wrong_letters)}',
                                        chat_id=chat_id,
                                        message_id=message_id)
        else:
            await bot.delete_message(chat_id=chat_id,
                                     message_id=message_id)
            await message.answer(text=f'Вы проиграли. :(\n'
                                      f'Слово было: {word}\n'
                                      f'Начните сначала.\n\n'
                                      f'{stages[hang_state]}\n\n'
                                      f'Неправильные буквы: {' '.join(wrong_letters)}',
                                 reply_markup=Keyboards.main_menu())

            users.update_one(filter={'user_id': user_id},
                             update={'$inc': {'losses': 1},
                                     '$set': {'win_streak': 0}})
            info = users.find_one({'user_id': user_id})

            wl = round(info['wins'] / info['losses'], 2)
            users.update_one(filter={'user_id': user_id},
                             update={'$set': {'WL': wl if wl != int(wl) else int(wl)}})

            await state.clear()
        return
    for i in find_all_indices(word, letter):
        text_word[i] = letter

    if is_it_a_win(word, text_word):
        await bot.delete_message(chat_id=chat_id,
                                 message_id=message_id)
        await bot.send_sticker(chat_id, choice(win_stickers))
        await message.answer(text=f'Вы выиграли. :)\n'
                                  f'Вы угадали слово: {word}\n'
                                  f'Начните сначала.\n\n'
                                  f'{stages[hang_state]}\n\n'
                                  f'Неправильные буквы: {' '.join(wrong_letters)}',
                             reply_markup=Keyboards.main_menu())

        users.update_one(filter={'user_id': user_id},
                         update={'$inc': {'wins': 1, 'win_streak': 1}})
        info = users.find_one({'user_id': user_id})

        if info['losses'] != 0:
            wl = round(info['wins'] / info['losses'], 2)
            users.update_one(filter={'user_id': user_id},
                             update={'$set': {'WL': wl if wl != int(wl) else int(wl)}})

        if info['max_win_streak'] < info['win_streak']:
            users.update_one(filter={'user_id': user_id},
                             update={'$set': {'max_win_streak': info['win_streak']}})

        await state.clear()
    else:
        await state.update_data(text_word=text_word)
        await bot.edit_message_text(text=f'Вы отгадали букву.\n'
                                         f'Поздравляю, вы на 1 шаг ближе к победе.\n\n'
                                         f'Осталось прав на ошибку: {6 + hang_state}\n\n'
                                         f'{' '.join(text_word)}\n\n'
                                         f'{stages[hang_state]}\n\n'
                                         f'Неправильные буквы: {' '.join(wrong_letters)}',
                                    chat_id=chat_id,
                                    message_id=message_id)


@dp.message()
async def message_deleter(message: Message):
    await message.delete()


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот завершил работу.')
