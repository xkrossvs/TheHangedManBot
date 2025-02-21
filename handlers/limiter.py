from aiogram.types import Message
from aiogram import Router, F
from handlers.game import GameProcess
from asyncio import sleep
from filters import IsTheWordWrong
from utils.units import remind_something

router = Router()


@router.message(GameProcess.word, IsTheWordWrong())
async def limit_word_state(message: Message):
    await message.delete()
    await remind_something(text='Отправьте слово нужной длины, состоящее из русских букв.', message=message)


@router.message(GameProcess.letter, F.text.len() > 1)
async def limit_letter_state(message: Message):
    await message.delete()
    await remind_something(text='Отправьте букву русского алфавита для продолжения игры.', message=message)
