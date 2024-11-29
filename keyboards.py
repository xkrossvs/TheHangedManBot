from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from strings import Strings
from themes import THEME_NAMES


class Keyboards:

    @staticmethod
    def main_menu() -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()
        builder.add(KeyboardButton(text=Strings.NEW_GAME_BUTTON))
        builder.add(KeyboardButton(text=Strings.PROFILE_BUTTON))
        builder.add(KeyboardButton(text=Strings.ACHIEVEMENTS_BUTTON))
        builder.add(KeyboardButton(text=Strings.LEADER_BOARD_BUTTON))
        builder.adjust(1, 3)
        return builder.as_markup(resize_keyboard=True,
                                 one_time_keyboard=True)

    @staticmethod
    def leader_board() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(text=Strings.WIN_LEADER_BOARD,
                                         callback_data=Strings.WIN_LEADER_BOARD))
        builder.add(InlineKeyboardButton(text=Strings.WL_LEADER_BOARD,
                                         callback_data=Strings.WL_LEADER_BOARD))
        builder.add(InlineKeyboardButton(text=Strings.MWS_LEADER_BOARD,
                                         callback_data=Strings.MWS_LEADER_BOARD))
        builder.adjust(1, 2)
        return builder.as_markup()

    @staticmethod
    def themes() -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()
        for theme in THEME_NAMES:
            builder.add(KeyboardButton(text=theme))
        builder.add(KeyboardButton(text=Strings.BACK_BUTTON))
        builder.adjust(2, 2, 1)
        return builder.as_markup(resize_keyboard=True)
