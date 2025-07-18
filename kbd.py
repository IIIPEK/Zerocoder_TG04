from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

async def build_keyboard(params,is_inline=True,url=False,adjust=2):
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
                                           one_time_keyboard=True,
                                           input_field_placeholder="Выберите действие..."
                                           )

reply_kbd = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="1"),
            KeyboardButton(text="2"),
            KeyboardButton(text="3"),
        ],
        [
            KeyboardButton(text="4"),
            KeyboardButton(text="5"),
            KeyboardButton(text="6"),
        ],
        [
            KeyboardButton(text="7"),
            KeyboardButton(text="8"),
            KeyboardButton(text="9"),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

inline_kbd = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="1", callback_data="1"),
            InlineKeyboardButton(text="2", callback_data="2"),
            InlineKeyboardButton(text="3", callback_data="3"),
        ],
        [
            InlineKeyboardButton(text="4", callback_data="4"),
            InlineKeyboardButton(text="5", callback_data="5"),
            InlineKeyboardButton(text="6", callback_data="6"),
        ],
        [
            InlineKeyboardButton(text="7", callback_data="7"),
            InlineKeyboardButton(text="8", callback_data="8"),
            InlineKeyboardButton(text="9", callback_data="9"),
        ],
    ]
)


start_kbd = ["Привет", "Пока",]

url_kbd = {"Video":"https://rutube.ru/video/efbddc56a5b2d403bfb0bec1327ebe0f/",
           "Music":"https://freemusicarchive.org/music/musinova/single/in-the-club-techno-housemp3/",
           "News":"https://dzen.ru/news",
           }

more_kbd = {"show_more":"Больше",
            }

options_kbd = {"opt_1":"Опция 1",
               "opt_2":"Опция 2",
              }
