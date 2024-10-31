from config import users, StatesData
from aiogram import Bot

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
        if achievement[0] == achievement[1]:
            await bot.send_message(chat_id=data['chat_id'],
                                   text=NOTIFICATION.format(name=name, description=achievement[2]))
            users.update_one(filter={'user_id': user_id},
                             update={'$set': {f'achievements.{name}': achievement}})

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
        if achievement[0] == achievement[1]:
            await bot.send_message(chat_id=data['chat_id'],
                                   text=NOTIFICATION.format(name=name, description=achievement[2]))
            users.update_one(filter={'user_id': user_id},
                             update={'$set': {f'achievements.{name}': achievement}})
