import asyncio
import logging
import sys
from config import TOKEN
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards import Keyboards
from strings import Strings
from words import words
from random import choice
from hangs import stages

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(text=f"Привет, {message.from_user.full_name}, и добро пожаловать в игру '<b>Висельница</b>'. "
                              f"Нажмите 'Начать игру', чтобы начать игру.",
                         reply_markup=Keyboards.main_menu())


@dp.message(F.text == Strings.START_GAME_BUTTON)
async def start_game_handler(message: Message) -> None:
    word = choice(words)
    len_word = len(word)
    await message.answer(text=f'Загадано слово из {len_word} букв.\n'
                              f'У вас есть право на 5 ошибок.\n\n'
                              f'{'_ ' * len_word}\n'
                              f'{stages[-1]}',
                         reply_markup=ReplyKeyboardRemove())


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
