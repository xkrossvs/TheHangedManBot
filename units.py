from config import users, LOG_GROUP_ID
from strings import Strings
from aiogram.types import TelegramObject
from aiogram import Bot
from datetime import datetime


def find_all_indices(word: str, char: str) -> list[int]:
    """
    :param word: загаданное слово
    :param char: отгаданная буква
    :return: индексы отгаданных букв в загаданном слове
    """
    return [i for i, letter in enumerate(word) if letter == char]


def is_it_a_win(word, text_word):
    return ''.join(text_word) == word


def leaderboard_generate(field: str, id_user: int) -> str:
    """Список возможных аргументов: max_win_streak, wins, WL."""
    users_data = users.find().sort(field, -1)
    user_leader_board = [[document['full_name'], document[field]] for document in users_data]
    message_text = Strings.LEADERS_TEXT[field]
    for place, info in enumerate(user_leader_board[:3]):
        message_text += f'{Strings.LEADER_BOARD_MEDALS[place]} <code>{info[0]}</code> ({info[1]})\n'
    message_text += f'\nВаша позиция: <b>{find_place(field, id_user)}</b>'
    return message_text


def find_place(field: str, id_user: int) -> int:
    """Список возможных аргументов: max_win_streak, wins, WL."""
    users_data = users.find().sort(field, -1)
    users_data = [document['user_id'] for document in users_data]
    for place, user_id in enumerate(users_data):
        if user_id == id_user:
            return place + 1


async def send_log(action: str, update: TelegramObject, bot: Bot):
    user_id = update.from_user.id
    username = update.from_user.username
    name = update.from_user.full_name
    time = datetime.now().strftime('%S.%f')[:-3]
    link = [name, f'<a href="t.me/{username}">{name}</a>']
    await bot.send_message(chat_id=LOG_GROUP_ID,
                           text=f'<u>{link[bool(username)]}</u> (id: <code>{user_id}</code>) {action}.\n'
                                f'<code>[{time}]</code>',
                           disable_web_page_preview=True)
