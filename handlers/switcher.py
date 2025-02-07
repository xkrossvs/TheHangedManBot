from aiogram.types import CallbackQuery
from aiogram import Router, F
from handlers.game import GameProcess
from data.strings import Strings
from keyboards import Keyboards
from aiogram.fsm.context import FSMContext

router = Router()


@router.callback_query(GameProcess.letter, F.data == Strings.LETTER_MODE_CALLBACK)
async def switch_letter_to_letter(callback: CallbackQuery):
    await callback.answer(text='⚠️ Вы и так в режиме отгадывания буквы.',
                          show_alert=True)


@router.callback_query(GameProcess.letter, F.data == Strings.WORD_MODE_CALLBACK)
async def switch_letter_to_word(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=Keyboards.guessing_mode_choice('word'))
    await state.set_state(GameProcess.word)


@router.callback_query(GameProcess.word, F.data == Strings.LETTER_MODE_CALLBACK)
async def switch_word_to_letter(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=Keyboards.guessing_mode_choice('letter'))
    await state.set_state(GameProcess.letter)


@router.callback_query(GameProcess.word, F.data == Strings.WORD_MODE_CALLBACK)
async def switch_word_to_word(callback: CallbackQuery):
    await callback.answer(text='⚠️ Вы и так в режиме отгадывания слова.',
                          show_alert=True)


@router.callback_query(F.data.in_((Strings.LETTER_MODE_CALLBACK, Strings.WORD_MODE_CALLBACK)))
async def no_switch(callback: CallbackQuery):
    await callback.answer()
