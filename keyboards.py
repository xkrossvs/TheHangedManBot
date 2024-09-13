from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
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
