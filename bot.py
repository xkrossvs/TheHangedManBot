import asyncio
import logging
import sys
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import achievements
import game
import leader_board
from config import MONGO_URL, TOKEN
from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.mongo import MongoStorage
from commands import set_commands

storage = MongoStorage.from_url(url=MONGO_URL, db_name='the_hanged_man')
dp = Dispatcher(storage=storage)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_router(leader_board.router)
    dp.include_router(game.router)
    dp.include_router(achievements.router)
    await set_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот завершил работу.')
