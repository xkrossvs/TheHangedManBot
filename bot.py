import asyncio
import logging
import sys
import pymongo
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from pymongo.collection import Collection
import game
from config import MONGO_URL, TOKEN
from aiogram import Dispatcher, Bot
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.mongo import MongoStorage

storage = MongoStorage.from_url(url=MONGO_URL, db_name='the_hanged_man')
dp = Dispatcher(storage=storage)
cluster = pymongo.MongoClient(MONGO_URL)
users: Collection = cluster.the_hanged_man.users


class GameProcess(StatesGroup):
    game = State()


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_router(game.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот завершил работу.')
