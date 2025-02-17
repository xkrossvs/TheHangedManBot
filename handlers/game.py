from random import choice
from datetime import datetime
from aiogram import F, Bot, Router
from aiogram.exceptions import TelegramForbiddenError
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, InputMediaPhoto, CallbackQuery
from data.themes import THEME_DICT, THEME_NAMES, THEMES, Theme
from config import users, ADMINS, LOG_GROUP_ID, hangs
from services.hangs import STAGES
from keyboards import Keyboards
from data.stickers import win_stickers
from data.strings import Strings, Game
from utils.units import find_all_indices, is_it_a_win, find_place, send_log, find_place_time, get_progress_bar_text, \
    get_progress_bar_info, convert_place_to_text, get_text, get_wrong_string
from utils.words import get_word_list
from filters import IsTheLetterRight, IsTheLetterWrong
from services.mongo_units import MongoUnits
from utils.achievement_units import AchievementUnits
from data.constants import ACHIEVEMENTS
import asyncio

router = Router()


class GameProcess(StatesGroup):
    letter = State()
    word = State()


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
    await message.answer(text=get_text('start'),
                         reply_markup=Keyboards.main_menu(),
                         disable_web_page_preview=True)
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
                          'min_time': None,
                          'achievements': ACHIEVEMENTS} | theme_inserter(THEMES))

        await send_log('зарегистрировался', message, bot)
        return
    # await send_log('нажал на старт', message, bot)


@router.message(Command('help'))
async def help_handler(message: Message):
    await message.answer(get_text('help'))


@router.message(Command('profile'))
@router.message(F.text == Strings.PROFILE_BUTTON)
async def profile_handler(message: Message, bot: Bot):
    user_id = message.from_user.id
    info = users.find_one({'user_id': user_id})
    time = f'{info['min_time']} сек.' if info['min_time'] else '—'
    achievements_amount = AchievementUnits.achievements_generator(user_id).count('✅')
    progress_bar = get_progress_bar_text(get_progress_bar_info(achievements_amount, len(ACHIEVEMENTS)))
    await message.answer(text=f'<blockquote>👤 {info["full_name"]}</blockquote>\n\n'
                              f'🔘 <u><b>Статистика</b></u>\n\n'
                              f'📯 Победы: <b>{info["wins"]}</b>\n'
                              f'☠️ Поражения: <b>{info["losses"]}</b>\n'
                              f'📊 Винрейт: <b>{info["WL"]}</b>\n'
                              f'🔥 Винстрик: <b>{info["win_streak"]}</b>\n'
                              f'⚡️ Максимальный винстрик: <b>{info["max_win_streak"]}</b>\n'
                              f'⌛️ Минимальное время: <b>{time}</b>\n\n'
                              f'🔘 <u><b>Достижения</b></u>\n\n'
                              f'🧩 Всего: <b>{achievements_amount} / {len(ACHIEVEMENTS)}</b>\n\n'
                              f'{progress_bar}\n\n'
                              f'🔘 <u><b>Место в рейтинге</b></u>\n\n'
                              f'📯 По победам: <b>{convert_place_to_text(find_place("wins", user_id))}</b>\n'
                              f'📊 По винрейту: <b>{convert_place_to_text(find_place("WL", user_id))}</b>\n'
                              f'🔥 По винстрику: <b>{convert_place_to_text(find_place("max_win_streak", user_id))}</b>\n'
                              f'⌛️ По скорости: <b>{convert_place_to_text(find_place_time(user_id))}</b>',
                         reply_markup=Keyboards.main_menu())
    await send_log('интересуется собой в профиле', message, bot)


@router.message(Command('new_game'))
@router.message(F.text == Strings.NEW_GAME_BUTTON)
async def new_game_handler(message: Message, bot: Bot):
    await message.answer(text='Выберите режим:\n\n'
                              f'<b>{Strings.SINGLEPLAYER_BUTTON}</b>: <i>отгадывайте слова самостоятельно.</i>\n\n'
                              f'<b>{Strings.MULTIPLAYER_BUTTON}</b>: <i>загадайте слово другу.</i>',
                         reply_markup=Keyboards.gamemode_choice())
    await send_log('выбирает режим игры', message, bot)


@router.message(F.text == Strings.MULTIPLAYER_BUTTON)
async def multiplayer_button(message: Message, bot: Bot):
    await message.answer(text=f'<b>{Strings.MULTIPLAYER_BUTTON}</b>\n\n'
                              f'Загадайте слово и добавьте при желании небольшую 💡 <i>подсказку</i>,'
                              f' чтобы другу было интереснее отгадывать.\n\n'
                              f'<blockquote><i>⚠️ Режим для двух игроков пока что не реализован.'
                              f' Поторопите разработчиков, чтобы ускорить процесс.</i></blockquote>',
                         reply_markup=Keyboards.multiplayer_hurry_button())
    await send_log('решил проверить дружеский режим', message, bot)


@router.callback_query(F.data == Strings.MULTIPLAYER_HURRY_BUTTON)
async def shop_hurry(callback: CallbackQuery, bot: Bot):
    await callback.answer(text='Спасибо! Мы работаем над этим режимом, а пока мы его делаем, поиграйте в одиночный.',
                          show_alert=True)
    await send_log('очень настойчиво требует режим для игры с друзьями', callback, bot)


@router.message(F.text == Strings.SINGLEPLAYER_BUTTON)
async def singleplayer_handler(message: Message, bot: Bot):
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

    await message.answer(text='📚 <b>Выбор темы</b>\n\n'
                              '<blockquote>🔤 <i>Слова</i> — общая категория без темы и подсказок. '
                              'Вам может попасться любое слово. '
                              'Режим не для всех.</blockquote>',
                         reply_markup=Keyboards.themes())
    # await send_log('выбрал путь одиночки и сейчас выбирает тему для игры', message, bot)


@router.message(F.text == Strings.BACK_BUTTON)
async def main_menu_handler(message: Message, bot: Bot) -> None:
    await message.answer(text='🖥 <b>Главное меню</b>',
                         reply_markup=Keyboards.main_menu())
    # await send_log('вернулся в главное меню', message, bot)


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
        await send_log(f'отыграл все слова в категории: {theme.name}❗️❗️❗️ @bonevis, @jevil_the_big_shot', message, bot)
        return

    loading_message = await message.answer(text='Загрузка...',
                                           reply_markup=ReplyKeyboardRemove())
    await bot.delete_message(chat_id=loading_message.chat.id,
                             message_id=loading_message.message_id)

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
    answer = await message.answer_photo(photo=STAGES[hang_state],
                                        caption=f'<i>слово</i>\n'
                                                f'{" ".join(text_word).replace('_', '◻️')}\n\n'
                                                f'<i>жизни</i>\n'
                                                f'{Strings.LIVES[-1]}\n\n'
                                                f'<i>ошибки</i>\n'
                                                f'{get_wrong_string(wrong_letters)}',
                                        reply_markup=Keyboards.guessing_mode_choice('letter'))
    users.update_one(filter={'user_id': user_id},
                     update={'$push': {f'{theme.used_words}': word}})
    chat_id = answer.chat.id
    await state.update_data(chat_id=chat_id)
    message_id = answer.message_id
    await state.update_data(message_id=message_id)
    start_time = datetime.now()
    await state.update_data(start_time=start_time)
    await state.set_state(GameProcess.letter)
    await send_log(f'начал игру в теме: {theme.name}', message, bot)


@router.message(GameProcess.letter, F.text.len() == 1, IsTheLetterRight())
async def right_letter(message: Message, bot: Bot, state: FSMContext, **data):
    user_id = message.from_user.id
    letter = message.text.upper()
    user = users.find_one(filter={'user_id': user_id})
    await message.delete()
    for i in find_all_indices(data['word'], letter):
        data['text_word'][i] = letter

    if is_it_a_win(data['word'], data['text_word']):
        await bot.edit_message_caption(caption=f'<i>слово</i>\n'
                                               f'{" ".join(data['text_word'])}\n\n'
                                               f'<i>жизни</i>\n'
                                               f'{Strings.LIVES[data['hang_state']]}\n\n'
                                               f'<i>ошибки</i>\n'
                                               f'{get_wrong_string(data['wrong_letters'])}',
                                       chat_id=data['chat_id'],
                                       message_id=data['message_id'],
                                       reply_markup=Keyboards.guessing_mode_choice('letter'))
        await bot.send_sticker(data['chat_id'], choice(win_stickers))
        await message.answer(text=Game.WIN_TEXT,
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
        time_of_win = round((datetime.now() - data['start_time']).total_seconds(), 2)
        if user['min_time'] is None or user['min_time'] > time_of_win:
            users.update_one(filter={'user_id': user_id},
                             update={'$set': {'min_time': time_of_win}})

        await state.clear()
    else:
        await state.update_data(text_word=data['text_word'])
        await bot.edit_message_caption(caption=f'<i>слово</i>\n'
                                               f'{" ".join(data['text_word']).replace('_', '◻️')}\n\n'
                                               f'<i>жизни</i>\n'
                                               f'{Strings.LIVES[data['hang_state']]}\n\n'
                                               f'<i>ошибки</i>\n'
                                               f'{get_wrong_string(data['wrong_letters'])}',
                                       chat_id=data['chat_id'],
                                       message_id=data['message_id'],
                                       reply_markup=Keyboards.guessing_mode_choice('letter'))
        await AchievementUnits.instant_insight_check(data, bot)
        # await send_log('отгадал букву', message, bot)


@router.message(GameProcess.letter, F.text.len() == 1, IsTheLetterWrong())
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
    media = InputMediaPhoto(media=STAGES[data['hang_state']],
                            caption=f'<i>слово</i>\n'
                                    f'{" ".join(data['text_word']).replace('_', '◻️')}\n\n'
                                    f'<i>жизни</i>\n'
                                    f'{Strings.LIVES[data['hang_state']]}\n\n'
                                    f'<i>ошибки</i>\n'
                                    f'{get_wrong_string(data['wrong_letters'])}')
    if data['hang_state'] != -7:
        await bot.edit_message_media(media=media,
                                     chat_id=data['chat_id'],
                                     message_id=data['message_id'],
                                     reply_markup=Keyboards.guessing_mode_choice('letter'))
        # await send_log('не отгадал букву', message, bot)
    else:
        await bot.edit_message_media(media=media,
                                     chat_id=data['chat_id'],
                                     message_id=data['message_id'],
                                     reply_markup=Keyboards.guessing_mode_choice('letter'))

        await message.answer(text=f'😐 Вы не отгадали слово:\n\n<b>{data['word']}</b>',
                             reply_markup=Keyboards.main_menu())
        await AchievementUnits.complete_disaster_check(data, bot)
        MongoUnits.lose_count_increase(user_id)
        MongoUnits.wl_negative_update(user_id)
        await AchievementUnits.success_series_check(data, bot)
        await AchievementUnits.champion_series_check(data, bot)
        await send_log('проиграл', message, bot)

        await state.clear()


@router.message(F.text)
async def message_text_deleter(message: Message, bot: Bot):
    await send_log(f'написал : {message.text}', message, bot)
    await message.delete()


@router.message(F.from_user.id.in_(ADMINS), F.photo, F.caption)
async def hang_photo_adder(message: Message):
    hangs.update_one(filter={'hang_number': int(message.caption)},
                     update={'$set': {'hang_id': message.photo[-1].file_id}})


@router.message(F.sticker | F.photo | F.video | F.document)
async def media_deleter(message: Message):
    await message.forward(LOG_GROUP_ID)

    await message.delete()
