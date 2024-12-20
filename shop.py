from aiogram import Router, F, Bot
from strings import Strings
from aiogram.types import Message, CallbackQuery
from keyboards import Keyboards
from units import send_log

router = Router()


@router.message(F.text == Strings.SHOP_BUTTON)
async def shop_button(message: Message, bot: Bot):
    await message.answer(text=f'{Strings.SHOP_BUTTON}\n\n'
                              f'Играйте и отгадывайте слова,'
                              f' чтобы заработать 🪙 <i>монетки</i>'
                              f' и улучшить вашу виселицу:'
                              f' цветочки, облачка и прочие украшения в нашем ассортименте.\n\n'
                              f'<blockquote><i>⚠️ Магазин закрыт на ремонт.'
                              f' Поторопите рабочих, чтобы ускорить процесс.</i></blockquote>',
                         reply_markup=Keyboards.shop_hurry_button())
    await send_log('пришел посмотреть магазин', message, bot)


@router.callback_query(F.data == Strings.SHOP_HURRY_BUTTON)
async def shop_hurry(callback: CallbackQuery, bot: Bot):
    await callback.answer(text='Спасибо! Мы работаем над этим и не заплатим рабочим, пока они не доделают магазин.',
                          show_alert=True)
    await send_log('очень настойчиво требует магазин', callback, bot)
