from typing import NamedTuple
from strings import ThemeButton


class Theme(NamedTuple):
    name: str
    words: str
    used_words: str


THEMES = [
    Theme(name=ThemeButton.WORDS, words='words', used_words='used_words'),
    Theme(name=ThemeButton.PROFESSIONS, words='professions', used_words='used_professions'),
    Theme(name=ThemeButton.TOWNS, words='towns', used_words='used_towns'),
    Theme(name=ThemeButton.MOVIES, words='movies', used_words='used_movies'),
]

THEME_DICT: dict[str, Theme] = {theme.name: theme for theme in THEMES}
THEME_NAMES: list[str] = [theme.name for theme in THEMES]
