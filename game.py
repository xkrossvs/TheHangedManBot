from random import choice

from aiogram import F, Bot, Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from config import users
from hangs import STAGES
from keyboards import Keyboards
from stickers import win_stickers
from strings import Strings, Game
from units import find_all_indices, is_it_a_win, find_place
from words import words
from filters import IsThereALetter

router = Router()


class GameProcess(StatesGroup):
    game = State()


@router.message(CommandStart())
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


@router.message(Command('profile'))
@router.message(F.text == Strings.PROFILE_BUTTON)
async def profile_handler(message: Message):
    user_id = message.from_user.id
    info = users.find_one({'user_id': user_id})
    await message.answer(text=f'Имя: {info["full_name"]}\n\n'
                              f'Количество побед: {info["wins"]}\n'
                              f'Количество поражений: {info["losses"]}\n'
                              f'Винрейт: {info["WL"]}\n'
                              f'Текущая серия побед: {info["win_streak"]}\n'
                              f'Максимальная серия побед: {info["max_win_streak"]}\n\n'
                              f'Место в рейтинге по победам: {find_place("wins", user_id)}\n'
                              f'Место в рейтинге по винрейту: {find_place("WL", user_id)}\n'
                              f'Место в рейтинге по винстрику: {find_place("max_win_streak", user_id)}',
                         reply_markup=Keyboards.main_menu())


@router.message(Command('new_game'))
@router.message(F.text == Strings.START_GAME_BUTTON)
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
                                       f'{" ".join(text_word)}\n'
                                       f'{STAGES[hang_state]}')
    users.update_one(filter={'user_id': user_id},
                     update={'$push': {'used_words': word}})
    chat_id = answer.chat.id
    await state.update_data(chat_id=chat_id)
    message_id = answer.message_id
    await state.update_data(message_id=message_id)
    await state.set_state(GameProcess.game)


@router.message(IsThereALetter(), F.text.len() == 1, GameProcess.game)
async def right_letter(message: Message, bot: Bot, state: FSMContext, **data):
    user_id = message.from_user.id
    letter = message.text.upper()
    await message.delete()
    for i in find_all_indices(data['word'], letter):
        data['text_word'][i] = letter

    if is_it_a_win(data['word'], data['text_word']):
        await bot.send_sticker(data['chat_id'], choice(win_stickers))
        await message.answer(text=Game.WIN_TEXT.format(word=data['word'],
                                                       hang_state=STAGES[data['hang_state']],
                                                       wrong_letters=" ".join(data['wrong_letters'])),
                             message_effect_id='5046509860389126442',
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
        await state.update_data(text_word=data['text_word'])
        await bot.edit_message_text(text=f'Вы отгадали букву.\n'
                                         f'Поздравляю, вы на 1 шаг ближе к победе.\n\n'
                                         f'Осталось прав на ошибку: {6 + data['hang_state']}\n\n'
                                         f'{" ".join(data['text_word'])}\n\n'
                                         f'{STAGES[data['hang_state']]}\n\n'
                                         f'Неправильные буквы: {" ".join(data['wrong_letters'])}',
                                    chat_id=data['chat_id'],
                                    message_id=data['message_id'])


@router.message(F.text.len() == 1, F.text.upper().in_(Strings.CYRILLIC_LETTERS), GameProcess.game)
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
            return
        wrong_letters.append(letter)
        await state.update_data(wrong_letters=wrong_letters)
        hang_state -= 1
        await state.update_data(hang_state=hang_state)
        if hang_state != -7:
            await bot.edit_message_text(text=f'Вы не отгадали букву.\n'
                                             f'Сожалею, вы на 1 шаг ближе к поражению.\n\n'
                                             f'Осталось прав на ошибку: {6 + hang_state}\n\n'
                                             f'{" ".join(text_word)}\n\n'
                                             f'{STAGES[hang_state]}\n\n'
                                             f'Неправильные буквы: {" ".join(wrong_letters)}',
                                        chat_id=chat_id,
                                        message_id=message_id)
        else:
            await message.delete()
            await message.answer(text=f'Вы проиграли. :(\n'
                                      f'Слово было: {word}\n'
                                      f'Начните сначала.\n\n'
                                      f'{STAGES[hang_state]}\n\n'
                                      f'Неправильные буквы: {" ".join(wrong_letters)}',
                                 reply_markup=Keyboards.main_menu())

            users.update_one(filter={'user_id': user_id},
                             update={'$inc': {'losses': 1},
                                     '$set': {'win_streak': 0}})
            info = users.find_one({'user_id': user_id})

            wl = round(info['wins'] / info['losses'], 2)
            users.update_one(filter={'user_id': user_id},
                             update={'$set': {'WL': wl if wl != int(wl) else int(wl)}})

            await state.clear()


@router.message()
async def message_deleter(message: Message):
    await message.delete()
