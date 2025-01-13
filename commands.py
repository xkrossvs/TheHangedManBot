from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram import Bot


async def set_commands(bot: Bot):
    commands = [BotCommand(command='new_game', description='🕹 Начать игру'),
                BotCommand(command='profile', description='👤 Профиль'),
                BotCommand(command='achievements', description='🧩 Достижения'),
                BotCommand(command='leader_board', description='🎖 Рейтинг'),
                BotCommand(command='start', description='🔄 Перезапуск'),
                BotCommand(command='help', description='❓ Помощь')]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
