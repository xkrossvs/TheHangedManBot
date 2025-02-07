from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from data.strings import Strings
from config import StatesData


class IsTheLetterRight(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext):
        data = await state.get_data()
        if message.text.upper() in data['word']:
            return data
        return False


class IsTheLetterWrong(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext):
        data = await state.get_data()
        letter = message.text.upper()
        if letter not in data['word'] and letter in Strings.CYRILLIC_LETTERS:
            return data
        return False


class IsTheWordWrong(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext):
        data: StatesData = await state.get_data()
        word = message.text.upper()
        if len(data['word']) != len(word):
            return data
        for letter in data['word']:
            if letter not in Strings.CYRILLIC_LETTERS:
                return data
        return False

