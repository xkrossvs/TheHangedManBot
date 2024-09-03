import asyncio
import logging
import sys
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

storage = MongoStorage.from_url(url=MONGO_URL, db_name='the_hanged_man')
dp = Dispatcher(storage=storage)


class GameProcess(StatesGroup):
    game = State()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(text=f"Привет, {message.from_user.full_name}, и добро пожаловать в игру '<b>Висельница</b>'. "
                              f"Нажмите 'Начать игру', чтобы начать игру.",
                         reply_markup=Keyboards.main_menu())


@dp.message(F.text == Strings.START_GAME_BUTTON)
async def start_game_handler(message: Message, state: FSMContext, bot: Bot) -> None:
    loading_message = await message.answer(text='Загрузка...',
                                           reply_markup=ReplyKeyboardRemove())
    await bot.delete_message(chat_id=loading_message.chat.id,
                             message_id=loading_message.message_id)
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
    chat_id = answer.chat.id
    await state.update_data(chat_id=chat_id)
    message_id = answer.message_id
    await state.update_data(message_id=message_id)
    await state.set_state(GameProcess.game)


@dp.message(F.text.len() == 1, F.text.upper().in_(Strings.CYRILLIC_LETTERS), GameProcess.game)
async def letter_catcher(message: Message, state: FSMContext, bot: Bot):
    await message.delete()
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
            await state.clear()
        return
    for i in find_all_indices(word, letter):
        text_word[i] = letter

    if is_it_a_win(word, text_word):
        await bot.delete_message(chat_id=chat_id,
                                 message_id=message_id)
        await message.answer(text=f'Вы выиграли. :)\n'
                                  f'Вы угадали слово: {word}\n'
                                  f'Начните сначала.\n\n'
                                  f'{stages[hang_state]}\n\n'
                                  f'Неправильные буквы: {' '.join(wrong_letters)}',
                             reply_markup=Keyboards.main_menu())
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
