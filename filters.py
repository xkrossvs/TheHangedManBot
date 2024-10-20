from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from typing import TypedDict


class StatesData(TypedDict):
    word: str
    chat_id: int
    text_word: list
    hang_state: int
    wrong_letters: str
    message_id: int


class IsTheLetterRight(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext):
        data = await state.get_data()
        if message.text.upper() in data['word']:
            return data
        else:
            return False


class IsTheLetterWrong(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext):
        data = await state.get_data()
        if message.text.upper() not in data['word']:
            return data
        else:
            return False
