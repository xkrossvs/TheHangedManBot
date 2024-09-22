from units import leaderboard_generate

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from keyboards import Keyboards
from strings import Strings


router = Router()


@router.message(F.text == Strings.LEADER_BOARD_BUTTON)
async def leader_board_message(message: Message):
    await message.answer(text='Выберите рейтинг, который хотите посмотреть:',
                         reply_markup=Keyboards.leader_board())


@router.callback_query(F.data == Strings.WIN_LEADER_BOARD)
async def win_leader_board_message(callback: CallbackQuery):
    await callback.message.edit_text(text=leaderboard_generate('wins'),
                                     reply_markup=Keyboards.leader_board())


@router.callback_query(F.data == Strings.WL_LEADER_BOARD)
async def win_leader_board_message(callback: CallbackQuery):
    await callback.message.edit_text(text=leaderboard_generate('WL'),
                                     reply_markup=Keyboards.leader_board())


@router.callback_query(F.data == Strings.MWS_LEADER_BOARD)
async def win_leader_board_message(callback: CallbackQuery):
    await callback.message.edit_text(text=leaderboard_generate('max_win_streak'),
                                     reply_markup=Keyboards.leader_board())
