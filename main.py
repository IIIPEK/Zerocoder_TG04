import os
import sqlite3
import random

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
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
        "Совет 3: Покупайте товары по скидкам и распродажам.",
        "Совет 4: Готовьте дома вместо посещения ресторанов.",
        "Совет 5: Используйте кэшбэк сервисы и накопительные карты.",
        "Совет 6: Покупайте товары оптом для экономии на единице товара.",
        "Совет 7: Отключите неиспользуемые подписки и сервисы.",
        "Совет 8: Сравнивайте цены в разных магазинах перед покупкой.",
        "Совет 9: Планируйте покупки заранее и составляйте списки.",
        "Совет 10: Экономьте на коммунальных услугах - выключайте свет и воду.",
        "Совет 11: Покупайте качественные вещи, которые прослужат дольше.",
        "Совет 12: Используйте общественный транспорт вместо такси.",
        "Совет 13: Ремонтируйте вещи вместо покупки новых.",
        "Совет 14: Покупайте сезонные товары в межсезонье.",
        "Совет 15: Избегайте импульсивных покупок - подумайте 24 часа.",
        "Совет 16: Используйте купоны и промокоды при онлайн покупках.",
        "Совет 17: Покупайте generic товары вместо брендовых аналогов.",
        "Совет 18: Выращивайте зелень и овощи на подоконнике или даче.",
        "Совет 19: Обменивайтесь вещами с друзьями вместо покупки новых.",
        "Совет 20: Автоматизируйте сбережения - настройте автоперевод на депозит.",
    ]
    tip = random.choice(tips)
    await message.answer(tip)

@dp.message(F.text == 'Личные финансы')
async def process_finance(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    is_user_exists = db_select(db_path, cond={"user_id": user_id})
    if not is_user_exists:
        await message.answer("Вы не зарегистрированы, сначала зарегистрируйтесь.")
        return
    await state.set_state(FinanceForm.cat1)
    await message.answer("Введите категорию расходов №1:")

@dp.message(FinanceForm.cat1)
async def process_categories(message: types.Message, state: FSMContext):
    await state.update_data(cat1 = message.text)
    await state.set_state(FinanceForm.costs1)
    await message.answer(f'Введите расходы для категории "{message.text}":')

@dp.message(FinanceForm.costs1)
async def process_costs(message: types.Message, state: FSMContext):
    await state.set_state(FinanceForm.cat2)
    await state.update_data(costs1 = float(message.text))
    await message.answer(f'Введите категорию расходов №2:')

@dp.message(FinanceForm.cat2)
async def process_categories(message: types.Message, state: FSMContext):
    await state.update_data(cat2 = message.text)
    await state.set_state(FinanceForm.costs2)
    await message.answer(f'Введите расходы для категории "{message.text}":')

@dp.message(FinanceForm.costs2)
async def process_costs(message: types.Message, state: FSMContext):
    await state.set_state(FinanceForm.cat3)
    await state.update_data(costs2 = float(message.text))
    await message.answer(f'Введите категорию расходов №3:')

@dp.message(FinanceForm.cat3)
async def process_categories(message: types.Message, state: FSMContext):
    await state.update_data(cat3 = message.text)
    await state.set_state(FinanceForm.costs3)
    await message.answer(f'Введите расходы для категории "{message.text}":')

@dp.message(FinanceForm.costs3)
async def process_costs(message: types.Message, state: FSMContext):
    await state.update_data(costs3 = float(message.text))
    data = await state.get_data()
    user_id = message.from_user.id
    if db_update(db_path, "users", data=data, cond={"user_id": user_id}):
        await message.answer("Данные успешно обновлены.")
        data = db_select(db_path, cond={"user_id": user_id})[0]
        await message.answer(f"Ваши категории расходов:\n{data[3]} - {data[6]};\n {data[4]} - {data[7]};\n {data[5]} - {data[8]}")
    else:
        await message.answer("Произошла ошибка при обновлении данных. Попробуйте снова.")
    await state.clear()



if __name__ == '__main__':
    dp.run_polling(bot)
