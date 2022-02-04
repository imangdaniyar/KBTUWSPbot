from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("help", "Вывести справку"),
            types.BotCommand("login", "Test Login WSP"),
            types.BotCommand("cancel", "Cancel authorization"),
            types.BotCommand("logout", "[Logged users] Logout"),
            types.BotCommand("menu", "[Logged users] Get WSP menu}"),

        ]
    )
