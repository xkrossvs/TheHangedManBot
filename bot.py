import asyncio
import logging
import sys
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from handlers import game, achievements, shop, leader_board, limiter, switcher, word_mode
from config import MONGO_URL, TOKEN
from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.mongo import MongoStorage
from commands import set_commands

storage = MongoStorage.from_url(url=MONGO_URL, db_name='the_hanged_man')
dp = Dispatcher(storage=storage)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_router(word_mode.router)
    dp.include_router(switcher.router)
    dp.include_router(limiter.router)
    dp.include_router(shop.router)
    dp.include_router(leader_board.router)
    dp.include_router(achievements.router)
    dp.include_router(game.router)
    await set_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот завершил работу.')
