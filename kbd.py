from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

async def build_keyboard(params,is_inline=True,url=False,adjust=2, one_time_keyboard=True):
    if is_inline:
        builder = InlineKeyboardBuilder()
        for param in params:
            if url:
                builder.add(InlineKeyboardButton(text=param, url=params[param]))
            else:
                builder.add(InlineKeyboardButton(text=params[param], callback_data=param))
        return builder.adjust(adjust).as_markup()
    else:
        builder = ReplyKeyboardBuilder()
        for param in params:
            builder.add(KeyboardButton(text=param))
        return builder.adjust(adjust).as_markup(resize_keyboard=True,
                                           one_time_keyboard=one_time_keyboard,
                                           input_field_placeholder="Выберите действие..."
                                           )


start_kbd = ["Привет", "Пока",]

url_kbd = {"Video":"https://rutube.ru/video/efbddc56a5b2d403bfb0bec1327ebe0f/",
           "Music":"https://freemusicarchive.org/music/musinova/single/in-the-club-techno-housemp3/",
           "News":"https://dzen.ru/news",
           }
main_kbd = ["Регистрация", "Курс валют", "Советы по экономии", "Личные финансы",]

more_kbd = {"show_more":"Больше",
            }

options_kbd = {"opt_1":"Опция 1",
               "opt_2":"Опция 2",
              }
