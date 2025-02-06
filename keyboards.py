from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from data.strings import Strings
from data.themes import THEME_NAMES


class Keyboards:

    @staticmethod
    def main_menu() -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()
        builder.add(KeyboardButton(text=Strings.NEW_GAME_BUTTON))
        builder.add(KeyboardButton(text=Strings.PROFILE_BUTTON))
        builder.add(KeyboardButton(text=Strings.ACHIEVEMENTS_BUTTON))
        builder.add(KeyboardButton(text=Strings.LEADER_BOARD_BUTTON))
        builder.add(KeyboardButton(text=Strings.SHOP_BUTTON))
        builder.adjust(1, 2, 2)
        return builder.as_markup(resize_keyboard=True,
                                 one_time_keyboard=False)

    @staticmethod
    def leader_board() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(text=Strings.WIN_LEADER_BOARD,
                                         callback_data=Strings.WIN_LEADER_BOARD))
        builder.add(InlineKeyboardButton(text=Strings.WL_LEADER_BOARD,
                                         callback_data=Strings.WL_LEADER_BOARD))
        builder.add(InlineKeyboardButton(text=Strings.MWS_LEADER_BOARD,
                                         callback_data=Strings.MWS_LEADER_BOARD))
        builder.add(InlineKeyboardButton(text=Strings.MIN_TIME_LEADER_BOARD,
                                         callback_data=Strings.MIN_TIME_LEADER_BOARD))
        builder.adjust(2, 2)
        return builder.as_markup()

    @staticmethod
    def themes() -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()
        for theme in THEME_NAMES:
            builder.add(KeyboardButton(text=theme))
        builder.add(KeyboardButton(text=Strings.BACK_BUTTON))
        builder.adjust(2, 2, 1)
        return builder.as_markup(resize_keyboard=True)

    @staticmethod
    def shop_hurry_button() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(text=Strings.SHOP_HURRY_BUTTON,
                                         callback_data=Strings.SHOP_HURRY_BUTTON))
        return builder.as_markup()

    @staticmethod
    def gamemode_choice() -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()
        builder.add(KeyboardButton(text=Strings.SINGLEPLAYER_BUTTON))
        builder.add(KeyboardButton(text=Strings.MULTIPLAYER_BUTTON))
        builder.adjust(2)
        return builder.as_markup(resize_keyboard=True)

    @staticmethod
    def multiplayer_hurry_button() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(text=Strings.MULTIPLAYER_HURRY_BUTTON,
                                         callback_data=Strings.MULTIPLAYER_HURRY_BUTTON))
        return builder.as_markup()

    @staticmethod
    def guessing_mode_choice(game_mode: str) -> InlineKeyboardMarkup:
        builder  = InlineKeyboardBuilder()
        if game_mode == 'letter':
            builder.add(InlineKeyboardButton(text=Strings.LETTER_MODE_BUTTON_ACTIVE,
                                             callback_data=Strings.LETTER_MODE_CALLBACK))
            builder.add(InlineKeyboardButton(text=Strings.WORD_MODE_BUTTON_INACTIVE,
                                             callback_data=Strings.WORD_MODE_CALLBACK))
        elif game_mode == 'word':
            builder.add(InlineKeyboardButton(text=Strings.LETTER_MODE_BUTTON_INACTIVE,
                                             callback_data=Strings.LETTER_MODE_CALLBACK))
            builder.add(InlineKeyboardButton(text=Strings.WORD_MODE_BUTTON_ACTIVE,
                                             callback_data=Strings.WORD_MODE_CALLBACK))
        return builder.as_markup()
