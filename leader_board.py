from aiogram.exceptions import TelegramBadRequest

from units import leaderboard_generate, send_log
from aiogram.filters import Command
from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from keyboards import Keyboards
from strings import Strings


router = Router()


@router.message(Command('leader_board'))
@router.message(F.text == Strings.LEADER_BOARD_BUTTON)
async def leader_board_message(message: Message):
    await message.answer(text='Выберите рейтинг, который хотите посмотреть:',
                         reply_markup=Keyboards.leader_board())


@router.callback_query(F.data == Strings.WIN_LEADER_BOARD)
async def win_leader_board_message(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    try:
        await callback.message.edit_text(text=leaderboard_generate('wins', user_id),
                                         reply_markup=Keyboards.leader_board())
    except TelegramBadRequest:
        await callback.answer('Вы и так здесь находитесь.')
    await send_log('интересуется рейтингом побед', callback, bot)


@router.callback_query(F.data == Strings.WL_LEADER_BOARD)
async def win_leader_board_message(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    try:
        await callback.message.edit_text(text=leaderboard_generate('WL', user_id),
                                         reply_markup=Keyboards.leader_board())
    except TelegramBadRequest:
        await callback.answer('Вы и так здесь находитесь.')
    await send_log('интересуется рейтингом винрейта', callback, bot)


@router.callback_query(F.data == Strings.MWS_LEADER_BOARD)
async def win_leader_board_message(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    try:
        await callback.message.edit_text(text=leaderboard_generate('max_win_streak', user_id),
                                         reply_markup=Keyboards.leader_board())
    except TelegramBadRequest:
        await callback.answer('Вы и так здесь находитесь.')
    await send_log('интересуется рейтингом винстрика', callback, bot)
