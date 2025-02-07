from datetime import datetime
from aiogram import F, Bot, Router
from aiogram.exceptions import TelegramForbiddenError
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, InputMediaPhoto, CallbackQuery
from data.themes import THEME_DICT, THEME_NAMES, THEMES, Theme
from config import users, ADMINS, LOG_GROUP_ID, hangs
from services.hangs import STAGES
from keyboards import Keyboards
from data.stickers import win_stickers
from data.strings import Strings, Game
from utils.units import find_all_indices, is_it_a_win, find_place, send_log, find_place_time, get_progress_bar_text, \
    get_progress_bar_info, convert_place_to_text, get_text, get_wrong_string
from utils.words import get_word_list
from filters import IsTheLetterRight, IsTheLetterWrong
from services.mongo_units import MongoUnits
from utils.achievement_units import AchievementUnits
from data.constants import ACHIEVEMENTS
from handlers.game import GameProcess

router = Router()


