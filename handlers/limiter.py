from aiogram.types import Message
from aiogram import Router, F
from handlers.game import GameProcess
from asyncio import sleep

router = Router()


@router.message(GameProcess.game, F.text.len() > 1)
async def limit_game_state(message: Message):
    await message.delete()
    note = await message.answer(text='Отправьте букву русского алфавита для продолжения игры.')
    await sleep(5)
    try:
        await note.delete()
    except:
        pass
