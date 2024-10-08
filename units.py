from config import users
from strings import Strings


def find_all_indices(word: str, char: str) -> list[int]:
    """
    :param word: загаданное слово
    :param char: отгаданная буква
    :return: индексы отгаданных букв в загаданном слове
    """
    return [i for i, letter in enumerate(word) if letter == char]


def is_it_a_win(word, text_word):
    return ''.join(text_word) == word


def leaderboard_generate(field: str):
    """Список возможных аргументов: max_win_streak, wins, WL."""
    users_data = users.find().sort(field, -1)
    user_leader_board = [[document['full_name'], document[field]] for document in users_data]
    message_text = Strings.LEADERS_TEXT[field]
    for place, info in enumerate(user_leader_board[:10]):
        message_text += f'{place + 1}.) {info[0]}: {info[1]}\n'
    return message_text


def find_place(field: str, id_user: int) -> int:
    """Список возможных аргументов: max_win_streak, wins, WL."""
    users_data = users.find().sort(field, -1)
    users_data = [document['user_id'] for document in users_data]
    for place, user_id in enumerate(users_data):
        if user_id == id_user:
            return place + 1
