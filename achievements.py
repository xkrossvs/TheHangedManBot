from aiogram.filters import Command
from aiogram import F, Router, Bot
from aiogram.types import Message
from strings import Strings
from achievement_units import AchievementUnits
from units import send_log

router = Router()


@router.message(Command('achievements'))
@router.message(F.text == Strings.ACHIEVEMENTS_BUTTON)
async def achievements_menu(message: Message, bot: Bot):
    user_id = message.from_user.id
    await message.answer(text=AchievementUnits.achievements_generator(user_id))
    await send_log('зашел полюбоваться своими достижениями', message, bot)
