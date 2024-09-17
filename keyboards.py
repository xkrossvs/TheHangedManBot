from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from strings import Strings


class Keyboards:

    @staticmethod
    def main_menu() -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()
        builder.add(KeyboardButton(text=Strings.START_GAME_BUTTON))
        builder.add(KeyboardButton(text=Strings.PROFILE_BUTTON))
        builder.add(KeyboardButton(text=Strings.LEADER_BOARD_BUTTON))
        return builder.as_markup(resize_keyboard=True,
                                 one_time_keyboard=True)

    @staticmethod
    def leader_board(buttons: list) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        for key in buttons:
            builder.add(InlineKeyboardButton(text=Strings.LEADERS_KEYBOARDS[key],
                                             callback_data=Strings.LEADERS_KEYBOARDS[key]))
        builder.adjust(*(1, 2) if len(buttons) == 3 else (2,))
        return builder.as_markup()
