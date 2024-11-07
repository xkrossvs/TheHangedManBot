class Strings:
    PROFILE_BUTTON = '👤 Профиль'
    START_GAME_BUTTON = '🕹 Начать игру'
    LEADER_BOARD_BUTTON = '🎖 Рейтинг'
    WIN_LEADER_BOARD = '📯 Победы'
    WL_LEADER_BOARD = '📊 Винрейт'
    MWS_LEADER_BOARD = '🔥 Винстрик'
    ACHIEVEMENTS_BUTTON = '🧩 Достижения'
    LEADERS_TEXT = {
        'wins': '🏆 <b>Рейтинг по победам</b>\n\n',
        'WL': '🏆 <b>Рейтинг по винрейту</b>\n\n',
        'max_win_streak': '🏆 <b>Рейтинг по винстрику</b>\n\n'
    }
    LEADERS_KEYBOARDS = {
        'wins': f'{WIN_LEADER_BOARD}',
        'WL': f'{WL_LEADER_BOARD}',
        'max_win_streak': f'{MWS_LEADER_BOARD}'
    }
    CYRILLIC_LETTERS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    LEADER_BOARD_MEDALS = ['🥇', '🥈', '🥉']
    LIVES = ['☠☠☠☠☠☠',
             '☠☠☠☠☠🤍',
             '☠☠☠☠🤍🤍',
             '☠☠☠🤍🤍🤍',
             '☠☠🤍🤍🤍🤍',
             '☠🤍🤍🤍🤍🤍',
             '🤍🤍🤍🤍🤍🤍'
             ]


class Game:
    WIN_TEXT = ('Вы выиграли. :)\n'
                '{lives}\n'
                'Вы угадали слово: {word}\n'
                'Начните сначала.\n\n'
                '{hang_state}\n\n'
                'Неправильные буквы: {wrong_letters}')
