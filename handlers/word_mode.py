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
from random import choice
from utils.units import find_all_indices, is_it_a_win, find_place, send_log, find_place_time, get_progress_bar_text, \
    get_progress_bar_info, convert_place_to_text, get_text, get_wrong_string
from utils.words import get_word_list
from filters import IsTheLetterRight, IsTheLetterWrong
from services.mongo_units import MongoUnits
from utils.achievement_units import AchievementUnits
from data.constants import ACHIEVEMENTS
from handlers.game import GameProcess

router = Router()


@router.message(GameProcess.word, F.text)
async def word_mode_handler(message: Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    user = users.find_one(filter={'user_id': user_id})
    data = await state.get_data()
    media = InputMediaPhoto(media=STAGES[-7],
                            caption=f'<i>слово</i>\n'
                                    f'{" ".join(data['text_word']).replace('_', '◻️')}\n\n'
                                    f'<i>жизни</i>\n'
                                    f'{Strings.LIVES[-7]}\n\n'
                                    f'<i>ошибки</i>\n'
                                    f'{get_wrong_string(data['wrong_letters'])}')
    await message.delete()
    if message.text.upper() == data['word']:
        data['text_word'] = list(data['word'])
        await bot.edit_message_caption(caption=f'<i>слово</i>\n'
                                               f'{" ".join(data['text_word'])}\n\n'
                                               f'<i>жизни</i>\n'
                                               f'{Strings.LIVES[data['hang_state']]}\n\n'
                                               f'<i>ошибки</i>\n'
                                               f'{get_wrong_string(data['wrong_letters'])}',
                                       chat_id=data['chat_id'],
                                       message_id=data['message_id'],
                                       reply_markup=Keyboards.guessing_mode_choice('word'))
        await bot.send_sticker(data['chat_id'], choice(win_stickers))
        time_of_win = round((datetime.now() - data['start_time']).total_seconds(), 2)
        await message.answer(text=Game.WIN_TEXT.format(time_of_win=time_of_win),
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
        if user['min_time'] is None or user['min_time'] > time_of_win:
            users.update_one(filter={'user_id': user_id},
                             update={'$set': {'min_time': time_of_win}})

        await state.clear()
        return

    await bot.edit_message_media(media=media,
                                 chat_id=data['chat_id'],
                                 message_id=data['message_id'],
                                 reply_markup=Keyboards.guessing_mode_choice('word'))

    await message.answer(text=f'😐 Вы не отгадали слово:\n\n<b>{data['word']}</b>',
                         reply_markup=Keyboards.main_menu())
    await AchievementUnits.complete_disaster_check(data, bot)
    MongoUnits.lose_count_increase(user_id)
    MongoUnits.wl_negative_update(user_id)
    await AchievementUnits.success_series_check(data, bot)
    await AchievementUnits.champion_series_check(data, bot)
    await send_log('проиграл', message, bot)

    await state.clear()

