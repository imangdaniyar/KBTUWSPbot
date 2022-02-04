import logging

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.inline.callback_data import cb_attestation
from keyboards.inline.menu import *
from loader import dp
from states.login import Login
from utils.wsp.user import WSPUser


@dp.callback_query_handler(cb_menu.filter(submenu='schedule'), state=Login.logged)
async def get_schedule_menu(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    logging.info(f'call = {callback_data}')
    await call.message.answer('Choose a day', reply_markup=schedule_menu)


@dp.callback_query_handler(cb_schedule.filter(submenu='schedule'), state=Login.logged)
async def get_schedule(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    logging.info(f'call = {callback_data}')
    day_name = callback_data.get('day_name')
    async with state.proxy() as data:
        daily_schedule = data['schedule'].get(day_name)
        if daily_schedule:
            courses = '\n'.join(daily_schedule)
            await call.message.answer(f'<b>{day_name.capitalize()}</b> :\n{courses}')
        else:
            await call.message.answer(f'<b>{day_name.capitalize()}</b> :\nNo courses')


@dp.callback_query_handler(cb_menu.filter(submenu='attestation'), state=Login.logged)
async def get_attestation_menu(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    logging.info(f'call = {callback_data}')
    await call.message.answer('Attestation:')
    attestation_menu = InlineKeyboardMarkup()
    async with state.proxy() as data:
        for semester in data['attestation'].keys():
            attestation_menu.add(
                InlineKeyboardButton(text=semester,
                                     callback_data=cb_attestation.new(submenu='attestation', semester=semester)))
    await call.message.answer('Choose semester', reply_markup=attestation_menu)


@dp.callback_query_handler(cb_attestation.filter(submenu='attestation'), state=Login.logged)
async def get_attestation(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    logging.info(f'call = {callback_data}')
    semester = callback_data.get('semester')
    print(semester)
    async with state.proxy() as data:
        await call.message.answer(semester)
        await call.message.answer_photo(photo=open(data['attestation'][semester], 'rb'))


@dp.callback_query_handler(cb_menu.filter(submenu='news'), state=Login.logged)
async def news(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    logging.info(f'call = {callback_data}')
    await call.message.answer('News:')
    async with state.proxy() as data:
        for i in data['news']:
            await call.message.answer(f'<b>Date:</b> \n{i["Date"]}\n<b>Description:</b>\n{i["Description"]}')


@dp.callback_query_handler(cb_menu.filter(submenu='attendance'), state=Login.logged)
async def attendance(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    logging.info(f'call = {callback_data}')
    await call.message.answer('Attendance:')
