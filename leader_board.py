from units import leaderboard_generate

from aiogram import F, Bot, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, Update
from config import users
from keyboards import Keyboards
from strings import Strings


router = Router()


@router.message(F.text == Strings.LEADER_BOARD_BUTTON)
async def leader_board_message(message: Message):
    await message.answer(text=leaderboard_generate('wins'))
