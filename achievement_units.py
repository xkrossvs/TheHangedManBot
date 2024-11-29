from datetime import datetime

from config import users, StatesData
from aiogram import Bot
from hangs import STAGES
from strings import ThemeButton

NOTIFICATION = ('✅ Получено достижение!\n\n'
                '<b>{name}</b>\n'
                '<i>{description}</i>')


class AchievementUnits:

    @staticmethod
    def achievements_generator(user_id: str | int) -> str:
        achievements: dict = users.find_one(filter={'user_id': user_id})['achievements']
        achievements_text = 'Список доступных достижений:\n\n'
        signs = ['✖️', '✅']
        for key, value in achievements.items():
            achievements_text += (f'{signs[value[0] == value[1]]}<b>{key}</b> ({value[0]} из {value[1]})\n'
                                  f'<i>{value[2]}</i>\n\n')
        return achievements_text

    @staticmethod
    async def complete_disaster_check(data: StatesData, bot: Bot):
        user_id = data['chat_id']
        user = users.find_one(filter={'user_id': user_id})
        name = '🥀 Полный Провал'
        achievement = user['achievements'][name]

        if achievement[0]:
            return

        if ''.join(data['text_word']).count('_') == len(data['word']):
            achievement[0] = 1
            await bot.send_message(chat_id=data['chat_id'],
                                   text=NOTIFICATION.format(name=name, description=achievement[2]))
            users.update_one(filter={'user_id': user_id},
                             update={'$set': {f'achievements.{name}': achievement}})

    @staticmethod
    async def success_series_check(data: StatesData, bot: Bot):
        user_id = data['chat_id']
        user = users.find_one(filter={'user_id': user_id})
        win_streak = user['win_streak']
        name = '🚀 Серия Успеха'
        achievement = user['achievements'][name]

        if achievement[0] == achievement[1]:
            return

        achievement[0] = win_streak
        users.update_one(filter={'user_id': user_id},
                         update={'$set': {f'achievements.{name}': achievement}})
        if achievement[0] == achievement[1]:
            await bot.send_message(chat_id=data['chat_id'],
                                   text=NOTIFICATION.format(name=name, description=achievement[2]))

    @staticmethod
    async def champion_series_check(data: StatesData, bot: Bot):
        user_id = data['chat_id']
        user = users.find_one(filter={'user_id': user_id})
        win_streak = user['win_streak']
        name = '🥇 Чемпионская Серия'
        achievement = user['achievements'][name]

        if achievement[0] == achievement[1]:
            return

        achievement[0] = win_streak
        users.update_one(filter={'user_id': user_id},
                         update={'$set': {f'achievements.{name}': achievement}})
        if achievement[0] == achievement[1]:
            await bot.send_message(chat_id=data['chat_id'],
                                   text=NOTIFICATION.format(name=name, description=achievement[2]))

    @staticmethod
    async def legendary_winner_check(data: StatesData, bot: Bot):
        user_id = data['chat_id']
        user = users.find_one(filter={'user_id': user_id})
        wins = user['wins']
        name = '🐉 Легендарный Победитель'
        achievement = user['achievements'][name]

        if achievement[0] == achievement[1]:
            return

        achievement[0] = wins
        users.update_one(filter={'user_id': user_id},
                         update={'$set': {f'achievements.{name}': achievement}})
        if achievement[0] == achievement[1]:
            await bot.send_message(chat_id=data['chat_id'],
                                   text=NOTIFICATION.format(name=name, description=achievement[2]))

    @staticmethod
    async def instant_insight_check(data: StatesData, bot: Bot):
        user_id = data['chat_id']
        user = users.find_one(filter={'user_id': user_id})
        name = '💫 Мгновенное Прозрение'
        achievement = user['achievements'][name]
        text_word = data['text_word']
        wrong_letters = data['wrong_letters']
        number_of_original_letters = set(''.join(text_word).replace('_', ''))

        if achievement[0] == achievement[1]:
            return
        if wrong_letters:
            return
        if text_word[0] == '_':
            return
        if len(number_of_original_letters) != 1:
            return

        achievement[0] = 1
        users.update_one(filter={'user_id': user_id},
                         update={'$set': {f'achievements.{name}': achievement}})
        if achievement[0] == achievement[1]:
            await bot.send_message(chat_id=data['chat_id'],
                                   text=NOTIFICATION.format(name=name, description=achievement[2]))

    @staticmethod
    async def without_a_miss_check(data: StatesData, bot: Bot):
        user_id = data['chat_id']
        user = users.find_one(filter={'user_id': user_id})
        name = '🔥 Без Промаха'
        achievement = user['achievements'][name]
        wrong_letters = data['wrong_letters']

        if achievement[0] == achievement[1]:
            return
        if wrong_letters:
            return

        achievement[0] = 1
        users.update_one(filter={'user_id': user_id},
                         update={'$set': {f'achievements.{name}': achievement}})
        if achievement[0] == achievement[1]:
            await bot.send_message(chat_id=data['chat_id'],
                                   text=NOTIFICATION.format(name=name, description=achievement[2]))

    @staticmethod
    async def bladerunner_check(data: StatesData, bot: Bot):
        user_id = data['chat_id']
        user = users.find_one(filter={'user_id': user_id})
        name = '🔪 Бегущий По Лезвию'
        achievement = user['achievements'][name]
        wrong_letters = data['wrong_letters']

        if achievement[0] == achievement[1]:
            return
        if len(wrong_letters) != len(STAGES) - 2:
            return

        achievement[0] = 1
        users.update_one(filter={'user_id': user_id},
                         update={'$set': {f'achievements.{name}': achievement}})
        if achievement[0] == achievement[1]:
            await bot.send_message(chat_id=data['chat_id'],
                                   text=NOTIFICATION.format(name=name, description=achievement[2]))

    @staticmethod
    async def da_vinci_code_check(data: StatesData, bot: Bot):
        user_id = data['chat_id']
        user = users.find_one(filter={'user_id': user_id})
        name = '📖 Код Да Винчи'
        achievement = user['achievements'][name]
        word = data['word']

        if achievement[0] == achievement[1]:
            return
        if len(word) < 7:
            return

        achievement[0] = 1
        users.update_one(filter={'user_id': user_id},
                         update={'$set': {f'achievements.{name}': achievement}})
        if achievement[0] == achievement[1]:
            await bot.send_message(chat_id=data['chat_id'],
                                   text=NOTIFICATION.format(name=name, description=achievement[2]))

    @staticmethod
    async def professional_check(data: StatesData, bot: Bot):
        user_id = data['chat_id']
        user = users.find_one(filter={'user_id': user_id})
        theme = data['theme']
        name = '🧑‍💼 Профессионал'
        achievement = user['achievements'][name]

        if theme != ThemeButton.PROFESSIONS:
            return

        if achievement[0] == achievement[1]:
            return

        achievement[0] += 1
        users.update_one(filter={'user_id': user_id},
                         update={'$set': {f'achievements.{name}': achievement}})
        if achievement[0] == achievement[1]:
            await bot.send_message(chat_id=data['chat_id'],
                                   text=NOTIFICATION.format(name=name, description=achievement[2]))

    @staticmethod
    async def cartographer_check(data: StatesData, bot: Bot):
        user_id = data['chat_id']
        user = users.find_one(filter={'user_id': user_id})
        theme = data['theme']
        name = '🗺 Картограф'
        achievement = user['achievements'][name]

        if theme != ThemeButton.TOWNS:
            return

        if achievement[0] == achievement[1]:
            return

        achievement[0] += 1
        users.update_one(filter={'user_id': user_id},
                         update={'$set': {f'achievements.{name}': achievement}})
        if achievement[0] == achievement[1]:
            await bot.send_message(chat_id=data['chat_id'],
                                   text=NOTIFICATION.format(name=name, description=achievement[2]))

    @staticmethod
    async def movie_fan_check(data: StatesData, bot: Bot):
        user_id = data['chat_id']
        user = users.find_one(filter={'user_id': user_id})
        theme = data['theme']
        name = '🎬 Киноман'
        achievement = user['achievements'][name]

        if theme != ThemeButton.MOVIES:
            return

        if achievement[0] == achievement[1]:
            return

        achievement[0] += 1
        users.update_one(filter={'user_id': user_id},
                         update={'$set': {f'achievements.{name}': achievement}})
        if achievement[0] == achievement[1]:
            await bot.send_message(chat_id=data['chat_id'],
                                   text=NOTIFICATION.format(name=name, description=achievement[2]))

    @staticmethod
    async def flash_check(data: StatesData, bot: Bot):
        user_id = data['chat_id']
        user = users.find_one(filter={'user_id': user_id})
        name = '⚡️ Флеш'
        achievement = user['achievements'][name]
        difference = (datetime.now() - data['start_time']).seconds

        if difference >= 20:
            return

        if achievement[0] == achievement[1]:
            return

        achievement[0] = 1
        users.update_one(filter={'user_id': user_id},
                         update={'$set': {f'achievements.{name}': achievement}})
        if achievement[0] == achievement[1]:
            await bot.send_message(chat_id=data['chat_id'],
                                   text=NOTIFICATION.format(name=name, description=achievement[2]))