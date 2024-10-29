from config import users, StatesData
from aiogram import Bot


class AchievementUnits:

    @staticmethod
    async def complete_disaster_check(data: StatesData, bot: Bot):
        user_id = data['chat_id']
        achievements = users.find_one(filter={'user_id': user_id})['achievements']
        if achievements['🥀 Полный Провал'][0]:
            return
        if ''.join(data['text_word']).count('_') == len(data['word']):
            achievements['🥀 Полный Провал'][0] = 1
            await bot.send_message(chat_id=data['chat_id'],
                                   text='Достижение получено: Полный провал.\n'
                                        'Проиграйте игру не угадав ни одной буквы.')
            users.update_one(filter={'user_id': user_id},
                             update={'$set': {'achievements': achievements}})
