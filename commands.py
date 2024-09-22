from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram import Bot

async def set_commands(bot: Bot):
    commands = [BotCommand(command='start_game', description='🕹 Начать игру'),
                BotCommand(command='profile', description='👤 Профиль'),
                BotCommand(command='leader_board', description='🎖 Рейтинг'),
                BotCommand(command='achievements', description='🧩 Достижения')]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
