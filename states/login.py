from aiogram.dispatcher.filters.state import StatesGroup, State


class Login(StatesGroup):
    login = State()
    password = State()


class UserState(StatesGroup):
    unauthorized = State()
    logged = State()
