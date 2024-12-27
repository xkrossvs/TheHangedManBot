from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from data.strings import Strings


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
        letter = message.text.upper()
        if letter not in data['word'] and letter in Strings.CYRILLIC_LETTERS:
            return data
        else:
            return False
