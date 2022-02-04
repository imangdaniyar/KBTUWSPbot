import logging
from aiogram.types import Message, CallbackQuery
from loader import dp


@dp.callback_query_handler(text='about')
async def get_about(call: CallbackQuery):
    await call.answer(cache_time=60)
    logging.info(f'call = about')
    await call.message.answer('KBTU WSP bot')
