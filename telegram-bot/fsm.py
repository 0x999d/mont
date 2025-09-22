from aiogram.fsm.state import State, StatesGroup


class AddURL(StatesGroup):
    url = State()
    interval = State()

class ChangeInterval(StatesGroup):
    interval = State()