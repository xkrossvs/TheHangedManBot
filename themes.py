from typing import NamedTuple
from strings import ThemeButton


class Theme(NamedTuple):
    name: str
    words: str
    used_words: str


themes = [
    Theme(name=ThemeButton.WORDS, words='words', used_words='used_words'),
    Theme(name=ThemeButton.PROFESSIONS, words='professions.txt', used_words='used_professions'),
    Theme(name=ThemeButton.TOWNS, words='towns', used_words='used_towns'),
    Theme(name=ThemeButton.MOVIES, words='movies.txt', used_words='used_movies'),
]

theme_dict: dict[str, Theme] = {theme.name: theme for theme in themes}

theme_names: list[str] = [theme.name for theme in themes]
