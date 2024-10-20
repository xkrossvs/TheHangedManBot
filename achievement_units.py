from config import users, StatesData
from aiogram import Bot


class AchievementUnits:

    @staticmethod
    async def complete_disaster_check(data: StatesData, bot: Bot):
        if ''.join(data['text_word']).count('_') == len(data['word']):
            await bot.send_message(chat_id=data['chat_id'],
                                   text='Достижение получено: Полный провал.\n'
                                        'Проиграйте игру не угадав ни одной буквы.')