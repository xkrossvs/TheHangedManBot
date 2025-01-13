from aiogram.exceptions import TelegramBadRequest

from utils.units import leaderboard_generate, send_log, leaderboard_generate_time
from aiogram.filters import Command
from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from keyboards import Keyboards
from data.strings import Strings


router = Router()


@router.message(Command('leader_board'))
@router.message(F.text == Strings.LEADER_BOARD_BUTTON)
async def leader_board_message(message: Message, bot: Bot):
    await message.answer(text='Выберите рейтинг, который хотите посмотреть:',
                         reply_markup=Keyboards.leader_board())
    await send_log('решил посмотреть рейтинги', message, bot)


@router.callback_query(F.data == Strings.WIN_LEADER_BOARD)
async def win_leader_board_message(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    try:
        await callback.message.edit_text(text=leaderboard_generate('wins', user_id),
                                         reply_markup=Keyboards.leader_board())
    except TelegramBadRequest:
        await callback.answer('Вы и так здесь находитесь.')
    # await send_log('интересуется рейтингом побед', callback, bot)


@router.callback_query(F.data == Strings.WL_LEADER_BOARD)
async def win_leader_board_message(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    try:
        await callback.message.edit_text(text=leaderboard_generate('WL', user_id),
                                         reply_markup=Keyboards.leader_board())
    except TelegramBadRequest:
        await callback.answer('Вы и так здесь находитесь.')
    # await send_log('интересуется рейтингом винрейта', callback, bot)


@router.callback_query(F.data == Strings.MWS_LEADER_BOARD)
async def win_leader_board_message(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    try:
        await callback.message.edit_text(text=leaderboard_generate('max_win_streak', user_id),
                                         reply_markup=Keyboards.leader_board())
    except TelegramBadRequest:
        await callback.answer('Вы и так здесь находитесь.')
    # await send_log('интересуется рейтингом винстрика', callback, bot)


@router.callback_query(F.data == Strings.MIN_TIME_LEADER_BOARD)
async def time_leader_board_message(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    try:
        await callback.message.edit_text(text=leaderboard_generate_time(user_id),
                                         reply_markup=Keyboards.leader_board())
    except TelegramBadRequest:
        await callback.answer('Вы и так здесь находитесь.')
    # await send_log('интересуется рейтингом времени', callback, bot)
