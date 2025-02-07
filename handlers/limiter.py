from aiogram.types import Message
from aiogram import Router, F
from handlers.game import GameProcess
from asyncio import sleep
from filters import IsTheWordWrong

router = Router()


@router.message(GameProcess.word, IsTheWordWrong())
async def limit_word_state(message: Message):
    await message.delete()
    note = await message.answer(text='Отправьте слово нужной длины, состоящее из русских букв.')
    await sleep(5)
    try:
        await note.delete()
    except:
        pass


@router.message(GameProcess.letter, F.text.len() > 1)
async def limit_letter_state(message: Message):
    await message.delete()
    note = await message.answer(text='Отправьте букву русского алфавита для продолжения игры.')
    await sleep(5)
    try:
        await note.delete()
    except:
        pass
