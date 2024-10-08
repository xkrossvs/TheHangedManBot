from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


class IsThereALetter(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext):
        data = await state.get_data()
        if message.text.upper() in data['word']:
            return {'word': data['word'],
                    'chat_id': data['chat_id'],
                    'text_word': data['text_word'],
                    'hang_state': data['hang_state'],
                    'wrong_letters': data['wrong_letters'],
                    'message_id': data['message_id']}
        else:
            return False
