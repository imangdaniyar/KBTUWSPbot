from aiogram.dispatcher.filters.builtin import CommandHelp, Command
from aiogram.types import Message, CallbackQuery

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: Message):
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку")
    await message.answer("\n".join(text))


@dp.callback_query_handler(text='help')
async def get_help(call: CallbackQuery):
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку")
    await call.message.answer("\n".join(text))
