from random import choice

from aiogram import F, Bot, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from config import users
from keyboards import Keyboards
from strings import Strings


router = Router()


@router.message(F.text == Strings.LEADER_BOARD_BUTTON)
async def leader_board_message(message: Message):
    users_wins = users.find().sort("wins", -1)
    user_leader_board = [[document['full_name'], document['wins']] for document in users_wins]
    message_text = 'Рейтинг по победам:\n\n'
    for place, info in enumerate(user_leader_board[:10]):
        message_text += f'{place + 1}.) {info[0]}: {info[1]}\n'
    await message.answer(text=message_text)

