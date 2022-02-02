import logging

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Command

from keyboards.inline.callback_data import cb_menu, cb_schedule
from keyboards.inline.menu import *
from loader import dp
from states.login import Login

schedule = {}


@dp.callback_query_handler(cb_menu.filter(submenu='schedule'))
async def schedule(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    logging.info(f'call = {callback_data}')
    await call.message.answer('Schedule:', reply_markup=schedule_menu)


@dp.callback_query_handler(cb_schedule.filter(submenu='schedule'))
async def schedule(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    logging.info(f'call = {callback_data}')
    day = callback_data.get('day_name')
    await call.message.answer(f'<b>{day}</b> :')


@dp.callback_query_handler(cb_menu.filter(submenu='attestation'))
async def attestation(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    logging.info(f'call = {callback_data}')
    await call.message.answer('Attestation:')


@dp.callback_query_handler(cb_menu.filter(submenu='news'))
async def news(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    logging.info(f'call = {callback_data}')
    await call.message.answer('News:')


@dp.callback_query_handler(cb_menu.filter(submenu='attendance'))
async def attendance(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    logging.info(f'call = {callback_data}')
    await call.message.answer('Attendance:')


@dp.callback_query_handler(text='login')
async def login(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    await Login.login.set()
    logging.info(f'call = {callback_data}')
    await call.message.answer('Login:')


@dp.message_handler(Command('login'))
async def fetch_wsp_info(message: Message):
    await Login.login.set()
    await message.reply('Login:')


@dp.message_handler(Command('cancel'), state='*')
async def cancel_handler(message: Message, state: FSMContext):
    if await state.get_state() is None:
        return
    await state.finish()


@dp.message_handler(state=Login.login)
async def fetch_login(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['login'] = message.text
    await Login.next()
    await message.reply('Password:')


@dp.message_handler(state=Login.password)
async def fetch_password(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['password'] = message.text
    async with state.proxy() as data:
        await message.answer(str({
            'login': data['login'],
            'password': data['password'],
            'telegram_id': message.from_user.id,
        }), reply_markup=wsp_menu)
    await state.finish()

# @dp.message_handler(commands=['get_attestation'], state=None)
# async def get_attestation(message: types.Message, state: FSMContext):
#     user = await conn.get_user(message.from_user.id)
#     wsp_user = WSPUser(login=user[0],
#                        password=user[1])
#     wsp_user.login()
#     attestation = wsp_user.get_attestation()
#     for i in attestation:
#         await bot.send_message(message.from_user.id, i)
#
#
# async def process_callback_schedule(callback_query: types.CallbackQuery):
#     await bot.answer_callback_query(callback_query.id)
#     global schedule
#     day = schedule.get(callback_query.data)
#     if day:
#         courses = '\n'.join(day)
#         await bot.send_message(callback_query.from_user.id, courses, parse_mode=ParseMode.MARKDOWN)
#     else:
#         await bot.send_message(callback_query.from_user.id, 'No courses', parse_mode=ParseMode.MARKDOWN)
#
#
# @dp.message_handler(commands=['get_schedule'], state=None)
# async def get_schedule(message: types.Message, state: FSMContext):
#     user = await conn.get_user(message.from_user.id)
#     wsp_user = WSPUser(login=user[0],
#                        password=user[1])
#     wsp_user.login()
#     global schedule
#     schedule = wsp_user.get_schedule()
#     keyboard = await wsp.get_schedule_keyboard()
#     await bot.send_message(message.from_user.id, 'Choose day:', reply_markup=keyboard)


# def register_handlers_user(dp: Dispatcher):
#     dp.register_callback_query_handler(process_callback_schedule, lambda c: c.data in wsp.day_names)
#     dp.register_message_handler(get_attestation, commands=['get_attestation'], state=None)
#     dp.register_message_handler(get_schedule, commands=['get_schedule'], state=None)
#     dp.register_message_handler(fetch_wsp_info, commands=['login'], state=None)
#     dp.register_message_handler(fetch_login, state=FSMUser.login)
#     dp.register_message_handler(fetch_password, state=FSMUser.password)
#     dp.register_message_handler(cancel_handler, commands=['cancel'], state='*')
