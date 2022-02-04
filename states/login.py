from aiogram.dispatcher.filters.state import StatesGroup, State


class Login(StatesGroup):
    login = State()
    password = State()
    logged = State()
