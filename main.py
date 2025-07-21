import os
import sqlite3
import random

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.filters.callback_data import CallbackData
from aiohttp import ClientSession

from dotenv import load_dotenv

from api import get_exchangerates
from common import FinanceForm
from kbd import build_keyboard, main_kbd
from utils import set_loglevel, group_countries_by_letter
from dbwork import db_select, db_add, db_create, db_update

S = "Lfyyst "

load_dotenv()
TOKEN = os.getenv('TOKEN')
set_loglevel(level=os.getenv('LOG_LEVEL', 'INFO'))
url = os.getenv('API_URL')
api_key = os.getenv('API_KEY')
url = url.replace('{API_KEY}', api_key)
db_path = os.getenv('DB_PATH')
db_create(db_path)


bot = Bot(token=TOKEN)
dp = Dispatcher()




@dp.message(Command(commands=['help']))
async def process_help_command(message: types.Message):
    await message.answer('''Я умею выполнять такие команды:
    /start - Запустить бота
    /help - Этот текст
    при запуске бота выдастся меню выбора
    ''')

@dp.message(CommandStart())
async def process_start_command(message: types.Message):
    keyboard = await build_keyboard(main_kbd, is_inline=False, one_time_keyboard=False)
    await message.answer("Привет! Я твой личный помощник. Выбери опцию в меню.\n", reply_markup= keyboard)

@dp.message(F.text == 'Регистрация')
async def process_start_registration(message: types.Message):
    user_id = message.from_user.id
    name = message.from_user.full_name
    is_user_exists = db_select(db_path, cond={"user_id": user_id})
    if not is_user_exists:
        if db_add(db_path, "users", {"user_id": user_id, "name": name}):
            await message.answer("Данные успешно добавлены.")
    else:
        await message.answer("Вы уже зарегистрированы")

@dp.message(F.text == 'Курс валют')
async def process_exchangerate(message: types.Message):
    async with ClientSession() as session:
        exchangerates = await get_exchangerates(url, session)
    if exchangerates:
        usd_rub = exchangerates.get('RUB', 0)
        usd_eur = exchangerates.get('EUR', 0)
        eur_rub = usd_rub / usd_eur
        await message.answer(f"Курс USD/RUB: {usd_rub:.2f}\nКурс EUR/RUB: {eur_rub:.2f}\nКурс EUR/USD: {usd_eur:.2f}")
    else:
        await message.answer("Не удалось получить курсы валют.")

@dp.message(F.text == 'Советы по экономии')
async def process_advice(message: types.Message):
    tips = [
        "Совет 1: Ведите бюджет и следите за своими расходами.",
        "Совет 2: Откладывайте часть доходов на сбережения.",
        "Совет 3: Покупайте товары по скидкам и распродажам."
    ]
    tip = random.choice(tips)
    await message.answer(tip)

if __name__ == '__main__':
    dp.run_polling(bot)
