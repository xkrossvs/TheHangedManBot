from config import users
from strings import Strings


def find_all_indices(word, char):
    return [i for i, letter in enumerate(word) if letter == char]


def is_it_a_win(word, text_word):
    return ''.join(text_word) == word


def leaderboard_generate(type: str):
    users_wins = users.find().sort(type, -1)
    user_leader_board = [[document['full_name'], document[type]] for document in users_wins]
    message_text = Strings.LEADERS_TEXT[type]
    for place, info in enumerate(user_leader_board[:10]):
        message_text += f'{place + 1}.) {info[0]}: {info[1]}\n'
    return message_text

