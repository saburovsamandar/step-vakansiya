# keyboards.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from languages import languages

def get_language_keyboard():
    kb = ReplyKeyboardBuilder()
    for lang in languages.values():
        kb.button(text=lang["lang_name"])
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)

def get_main_menu(lang_code):
    lang = languages[lang_code]
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=lang["add_vacancy"])]],
        resize_keyboard=True
    )
    return kb
