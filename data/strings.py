class Strings:
    PROFILE_BUTTON = '👤 Профиль'
    NEW_GAME_BUTTON = '🕹 Начать игру'
    SINGLEPLAYER_BUTTON = '👤 1 игрок'
    MULTIPLAYER_BUTTON = '👥 2 игрока'
    LETTER_MODE_BUTTON_INACTIVE = '🔴 Буквы'
    LETTER_MODE_BUTTON_ACTIVE = '🟢 Буквы'
    WORD_MODE_BUTTON_INACTIVE = '🔴 Слово'
    WORD_MODE_BUTTON_ACTIVE = '🟢 Слово'
    LETTER_MODE_CALLBACK = 'letter_game_mode'
    WORD_MODE_CALLBACK = 'word_game_mode'
    LEADER_BOARD_BUTTON = '🎖 Рейтинг'
    WIN_LEADER_BOARD = '📯 Победы'
    WL_LEADER_BOARD = '📊 Винрейт'
    MWS_LEADER_BOARD = '🔥 Винстрик'
    MIN_TIME_LEADER_BOARD = '⌛️ Скорость'
    ACHIEVEMENTS_BUTTON = '🧩 Достижения'
    BACK_BUTTON = '↩️ Назад'
    SHOP_BUTTON = '🏪 Магазин'
    SHOP_HURRY_BUTTON = '🗣 Поторопить рабочих!'
    MULTIPLAYER_HURRY_BUTTON = '🗣 Поторопить разработчиков!'
    LEADERS_TEXT = {
        'min_time': '🏆 <b>Рейтинг по скорости</b>\n\n',
        'wins': '🏆 <b>Рейтинг по победам</b>\n\n',
        'WL': '🏆 <b>Рейтинг по винрейту</b>\n\n',
        'max_win_streak': '🏆 <b>Рейтинг по винстрику</b>\n\n'
    }
    LEADERS_KEYBOARDS = {
        'min_time': f'{MIN_TIME_LEADER_BOARD}',
        'wins': f'{WIN_LEADER_BOARD}',
        'WL': f'{WL_LEADER_BOARD}',
        'max_win_streak': f'{MWS_LEADER_BOARD}'
    }
    CYRILLIC_LETTERS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    LEADER_BOARD_MEDALS = ['🥇', '🥈', '🥉']
    LIVES = ['☠ ☠ ☠ ☠ ☠ ☠',
             '☠ ☠ ☠ ☠ ☠ 🤍',
             '☠ ☠ ☠ ☠ 🤍 🤍',
             '☠ ☠ ☠ 🤍 🤍 🤍',
             '☠ ☠ 🤍 🤍 🤍 🤍',
             '☠ 🤍 🤍 🤍 🤍 🤍',
             '🤍 🤍 🤍 🤍 🤍 🤍'
             ]


class Game:
    WIN_TEXT = 'Слово отгадано! <code>({time_of_win} сек.)</code>\n\n<b>Победа</b> 🔥'


class ThemeButton:
    WORDS = '🔤 Слова'
    PROFESSIONS = '👷🏻 Профессии'
    TOWNS = '🏙 Города'
    MOVIES = '🎬 Фильмы'
