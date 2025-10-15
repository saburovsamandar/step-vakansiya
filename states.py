# states.py

from aiogram.fsm.state import StatesGroup, State

class VacancyForm(StatesGroup):
    waiting_for_field = State()
    current_field = State()
