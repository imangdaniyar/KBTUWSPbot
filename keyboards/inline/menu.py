from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.callback_data import cb_schedule, cb_menu

main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Login WSP',
                              callback_data='login')],
        [InlineKeyboardButton(text='Settings',
                              callback_data='settings')],
        [InlineKeyboardButton(text='Help',
                              callback_data='help')],
        [InlineKeyboardButton(text='About',
                              callback_data='about')],
    ]
)

wsp_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Get attestation',
                              callback_data=cb_menu.new(submenu='attestation'))],
        [InlineKeyboardButton(text='Get schedule',
                              callback_data=cb_menu.new(submenu='schedule'))],
        [InlineKeyboardButton(text='Get news',
                              callback_data=cb_menu.new(submenu='news'))],
        [InlineKeyboardButton(text='Attend lesson',
                              callback_data=cb_menu.new(submenu='attendance'))],
    ]
)

schedule_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Понедельник',
                                 callback_data=cb_schedule.new(
                                     submenu='schedule',
                                     day_name='monday')
                                 ),
            InlineKeyboardButton(text='Вторник',
                                 callback_data=cb_schedule.new(
                                     submenu='schedule',
                                     day_name='tuesday')
                                 ),
            InlineKeyboardButton(text='Среда',
                                 callback_data=cb_schedule.new(
                                     submenu='schedule',
                                     day_name='wednesday')
                                 )
        ],
        [
            InlineKeyboardButton(text='Четверг',
                                 callback_data=cb_schedule.new(
                                     submenu='schedule',
                                     day_name='thursday')
                                 ),
            InlineKeyboardButton(text='Пятница',
                                 callback_data=cb_schedule.new(
                                     submenu='schedule',
                                     day_name='friday')
                                 ),
            InlineKeyboardButton(text='Суббота',
                                 callback_data=cb_schedule.new(
                                     submenu='schedule',
                                     day_name='saturday')
                                 )
        ],
        [
            InlineKeyboardButton(text='Воскресенье',
                                 callback_data=cb_schedule.new(
                                     submenu='schedule',
                                     day_name='sunday')
                                 )
        ]
    ]
)

attestation_menu = InlineKeyboardMarkup()
