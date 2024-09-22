from aiogram.filters import Command
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from keyboards import Keyboards
from strings import Strings

router = Router()


@router.message(Command('achievements'))
@router.message(F.text == Strings.ACHIEVEMENTS_BUTTON)
async def achievements_menu(message: Message):
    await message.answer(text='тут будут достижения')