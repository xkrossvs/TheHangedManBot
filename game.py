from random import choice
from datetime import datetime
from aiogram import F, Bot, Router
from aiogram.exceptions import TelegramForbiddenError
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, InputMediaPhoto
from themes import THEME_DICT, THEME_NAMES, THEMES, Theme
from config import users, ADMINS, LOG_GROUP_ID
from hangs import STAGES
from keyboards import Keyboards
from stickers import win_stickers
from strings import Strings, Game
from units import find_all_indices, is_it_a_win, find_place, send_log
from words import get_word_list
from filters import IsTheLetterRight, IsTheLetterWrong
from mongo_units import MongoUnits
from achievement_units import AchievementUnits
from constants import ACHIEVEMENTS
import asyncio

router = Router()


class GameProcess(StatesGroup):
    game = State()


class MailingProcess(StatesGroup):
    mailing = State()


@router.message(F.from_user.id.in_(ADMINS), F.text.lower() == 'рассылка')
async def mailing_starter(message: Message, state: FSMContext):
    await message.answer('Напишите, что вы хотите всем разослать.')
    await state.set_state(MailingProcess.mailing)


@router.message(MailingProcess.mailing)
async def mailing_process(message: Message, state: FSMContext, bot: Bot):
    for user in users.find():
        chat_id = user['user_id']
        try:
            if chat_id != message.from_user.id:
                await message.send_copy(chat_id=chat_id)
        except TelegramForbiddenError:
            await bot.send_message(text=f'<u>{user['full_name']}</u> (id: <code>{chat_id}</code>) '
                                        f'заблокировал бота и будет удалён из БД.\n',
                                   chat_id=LOG_GROUP_ID)
            users.delete_one(filter={'user_id': chat_id})
        await asyncio.sleep(0.05)
    await message.answer('Рассылка завершена.')
    await state.clear()


@router.message(CommandStart())
async def command_start_handler(message: Message, bot: Bot):
    await message.answer(text=f"Привет, {message.from_user.full_name}, и добро пожаловать в игру '<b>Висельница</b>'. "
                              f"Нажмите 'Начать игру', чтобы начать игру.",
                         reply_markup=Keyboards.main_menu())
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    if not users.find_one({'user_id': user_id}):
        def theme_inserter(themes: list) -> dict:
            theme_dict = {}
            for theme in themes:
                theme_dict[theme.used_words] = []
            return theme_dict

        users.insert_one({'user_id': user_id, 'full_name': full_name,
                          'wins': 0, 'losses': 0, 'WL': 0,
                          'win_streak': 0, 'max_win_streak': 0,
                          'achievements': ACHIEVEMENTS} | theme_inserter(THEMES))

        await send_log('зарегистрировался', message, bot)
        return
    await send_log('нажал на старт', message, bot)


@router.message(Command('profile'))
@router.message(F.text == Strings.PROFILE_BUTTON)
async def profile_handler(message: Message, bot: Bot):
    user_id = message.from_user.id
    info = users.find_one({'user_id': user_id})
    achievements_amount = AchievementUnits.achievements_generator(user_id).count('✅')
    await message.answer(text=f'<blockquote>👤 {info["full_name"]}</blockquote>\n\n'
                              f'〰️ <i>Статистика</i> 〰️\n\n'
                              f'📯 Победы: <b>{info["wins"]}</b>\n'
                              f'☠️ Поражения: <b>{info["losses"]}</b>\n'
                              f'📊 Винрейт: <b>{info["WL"]}</b>\n'
                              f'🔥 Винстрик: <b>{info["win_streak"]}</b>\n'
                              f'⚡️ Максимальный винстрик: <b>{info["max_win_streak"]}</b>\n'
                              f'🧩 Достижения: <b>{achievements_amount} / {len(ACHIEVEMENTS)}</b>\n\n'
                              f'〰️ <i>Место в рейтинге</i> 〰️\n\n'
                              f'📯 По победам: <b>{find_place("wins", user_id)}</b>\n'
                              f'📊 По винрейту: <b>{find_place("WL", user_id)}</b>\n'
                              f'🔥 По винстрику: <b>{find_place("max_win_streak", user_id)}</b>',
                         reply_markup=Keyboards.main_menu())
    await send_log('интересуется собой в профиле', message, bot)


# TODO: исключить попытки выйти из игры во время угадывания
# TODO: поменять текст
@router.message(Command('new_game'))
@router.message(F.text == Strings.NEW_GAME_BUTTON)
async def new_game_handler(message: Message, bot: Bot):
    user_id = message.from_user.id
    user = users.find_one(filter={'user_id': user_id})
    achievements = user['achievements']

    for theme in THEMES:
        if theme.used_words not in user:
            users.update_one(filter={'user_id': user_id},
                             update={'$set': {f'{theme.used_words}': []}})

    for achievement in ACHIEVEMENTS:
        if achievement not in achievements:
            achievements[achievement] = ACHIEVEMENTS[achievement]
    users.update_one(filter={'user_id': user_id},
                     update={'$set': {'achievements': achievements}})

    await message.answer(text='Выберите тему',
                         reply_markup=Keyboards.themes())
    await send_log('выбирает тему для игры', message, bot)


# TODO: поменять текст
@router.message(F.text == Strings.BACK_BUTTON)
async def main_menu_handler(message: Message, bot: Bot) -> None:
    await message.answer(text='Главное меню',
                         reply_markup=Keyboards.main_menu())
    await send_log('вернулся в главное меню', message, bot)


@router.message(F.text.in_(THEME_NAMES))
async def start_game_handler(message: Message, state: FSMContext, bot: Bot) -> None:
    user_id = message.from_user.id
    theme: Theme = THEME_DICT.get(message.text)
    await state.update_data(theme=message.text)
    words = get_word_list(theme.words)
    used_words = users.find_one({'user_id': user_id})[theme.used_words]

    if len(words) == len(used_words):
        await message.answer(text='У вас закончились слова в этой категории',
                             reply_markup=Keyboards.themes())
        await send_log(f'отыграл все слова в категории: {theme.name}', message, bot)
        return

    loading_message = await message.answer(text='Загрузка...',
                                           reply_markup=ReplyKeyboardRemove())
    await bot.delete_message(chat_id=loading_message.chat.id,
                             message_id=loading_message.message_id)

    word = choice(words)
    while word in used_words:
        word = choice(words)
    print(word)
    # TODO: убрать принт после разработки
    await state.update_data(word=word)
    text_word = ['_'] * len(word)
    await state.update_data(text_word=text_word)
    hang_state = -1
    await state.update_data(hang_state=hang_state)
    wrong_letters = []
    await state.update_data(wrong_letters=wrong_letters)
    answer = await message.answer_photo(photo=STAGES[hang_state],
                                        caption=f'Загадано слово из {len(word)} букв.\n'
                                                f'{Strings.LIVES[hang_state]}\n\n'
                                                f'{" ".join(text_word).replace('_', '◻️')}\n')
    users.update_one(filter={'user_id': user_id},
                     update={'$push': {f'{theme.used_words}': word}})
    chat_id = answer.chat.id
    await state.update_data(chat_id=chat_id)
    message_id = answer.message_id
    await state.update_data(message_id=message_id)
    start_time = datetime.now()
    await state.update_data(start_time=start_time)
    await state.set_state(GameProcess.game)
    await send_log(f'начал игру в теме: {theme.name}', message, bot)


@router.message(IsTheLetterRight(), F.text.len() == 1, GameProcess.game)
async def right_letter(message: Message, bot: Bot, state: FSMContext, **data):
    user_id = message.from_user.id
    letter = message.text.upper()
    await message.delete()
    for i in find_all_indices(data['word'], letter):
        data['text_word'][i] = letter

    if is_it_a_win(data['word'], data['text_word']):
        await bot.delete_message(chat_id=data['chat_id'],
                                 message_id=data['message_id'])
        await bot.send_sticker(data['chat_id'], choice(win_stickers))
        await message.answer_photo(photo=STAGES[data['hang_state']],
                                   caption=Game.WIN_TEXT.format(word=data['word'],
                                                                lives=Strings.LIVES[data['hang_state']],
                                                                wrong_letters=" ".join(data['wrong_letters'])),
                                   message_effect_id='5046509860389126442',
                                   reply_markup=Keyboards.main_menu())

        MongoUnits.win_count_increase(user_id)
        MongoUnits.wl_and_mws_update(user_id)
        await AchievementUnits.success_series_check(data, bot)
        await AchievementUnits.champion_series_check(data, bot)
        await AchievementUnits.legendary_winner_check(data, bot)
        await AchievementUnits.without_a_miss_check(data, bot)
        await AchievementUnits.bladerunner_check(data, bot)
        await AchievementUnits.da_vinci_code_check(data, bot)
        await AchievementUnits.cartographer_check(data, bot)
        await AchievementUnits.movie_fan_check(data, bot)
        await AchievementUnits.professional_check(data, bot)
        await AchievementUnits.flash_check(data, bot)
        await send_log('победил', message, bot)

        await state.clear()
    else:
        await state.update_data(text_word=data['text_word'])
        await bot.edit_message_caption(caption=f'Вы отгадали букву.\n'
                                               f'Поздравляю, вы на 1 шаг ближе к победе.\n\n'
                                               f'{Strings.LIVES[data['hang_state']]}\n\n'
                                               f'{" ".join(data['text_word']).replace('_', '◻️')}\n\n'
                                               f'Неправильные буквы: {" ".join(data['wrong_letters'])}',
                                       chat_id=data['chat_id'],
                                       message_id=data['message_id'])
        await AchievementUnits.instant_insight_check(data, bot)
        await send_log('отгадал букву', message, bot)


@router.message(IsTheLetterWrong(), F.text.len() == 1, GameProcess.game)
async def wrong_letter(message: Message, state: FSMContext, bot: Bot, **data):
    await message.delete()
    user_id = message.from_user.id
    letter = message.text.upper()

    if letter in data['wrong_letters']:
        return
    data['wrong_letters'].append(letter)
    await state.update_data(wrong_letters=data['wrong_letters'])
    data['hang_state'] -= 1
    await state.update_data(hang_state=data['hang_state'])
    if data['hang_state'] != -7:
        media = InputMediaPhoto(media=STAGES[data['hang_state']],
                                caption=f'Вы не отгадали букву.\n'
                                        f'Сожалею, вы на 1 шаг ближе к поражению.\n\n'
                                        f'{Strings.LIVES[data['hang_state']]}\n\n'
                                        f'{" ".join(data['text_word']).replace('_', '◻️')}\n\n'
                                        f'Неправильные буквы: {" ".join(data['wrong_letters'])}')
        await bot.edit_message_media(media=media,
                                     chat_id=data['chat_id'],
                                     message_id=data['message_id'])
        await send_log('не отгадал букву', message, bot)
    else:
        await bot.delete_message(chat_id=data['chat_id'],
                                 message_id=data['message_id'])

        await message.answer_photo(photo=STAGES[data['hang_state']],
                                   caption=f'Вы проиграли. :(\n'
                                           f'{Strings.LIVES[data['hang_state']]}\n'
                                           f'Слово было: {data['word']}\n'
                                           f'Начните сначала.\n\n'
                                           f'Неправильные буквы: {" ".join(data['wrong_letters'])}',
                                   reply_markup=Keyboards.main_menu())
        await AchievementUnits.complete_disaster_check(data, bot)
        MongoUnits.lose_count_increase(user_id)
        MongoUnits.wl_negative_update(user_id)
        await AchievementUnits.success_series_check(data, bot)
        await AchievementUnits.champion_series_check(data, bot)
        await send_log('проиграл', message, bot)

        await state.clear()


@router.message()
async def message_deleter(message: Message):
    await message.delete()
