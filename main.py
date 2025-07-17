import asyncio
import logging
import os



from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiohttp import ClientSession

from dotenv import load_dotenv

from kbd import more_kbd, options_kbd, url_kbd, start_kbd, build_keyboard
from utils import set_loglevel, group_countries_by_letter
from api import get_countries_list, countries_cache

load_dotenv()
TOKEN = os.getenv('TOKEN')
set_loglevel(level=os.getenv('LOG_LEVEL', 'INFO'))
url = os.getenv('API_URL')


bot = Bot(token=TOKEN)
dp = Dispatcher()

class LetterCallback(CallbackData, prefix="letter"):
    letter: str

class CountryCallback(CallbackData, prefix="country"):
    code: str

class BackCallback(CallbackData, prefix="back"):
    to: str  # "main" или "letters"

async def create_letters_menu():
    async with ClientSession() as session:
        countries = await get_countries_list(url, session)
    letters = group_countries_by_letter(countries)
    letter_menu = {LetterCallback(letter=x).pack():f"{x}({len(letters[x])})" for x in letters.keys()}
    return await build_keyboard(letter_menu, is_inline=True, adjust=6)


async def create_countries_menu(letter):
    async with ClientSession() as session:
        countries = await get_countries_list(url, session)
    if not countries:
        return None

    grouped_countries = group_countries_by_letter(countries)
    countries_for_letter = grouped_countries.get(letter, [])

    keyboard = {}

    for country in countries_for_letter:
        keyboard[CountryCallback(code=country['code']).pack()] = country['name']
    # Добавляем кнопку "Назад"
    keyboard[BackCallback(to="main").pack()] = "⬅️ Назад к буквам"
    return await build_keyboard(keyboard, is_inline=True, adjust=4)

@dp.message(Command(commands=['help']))
async def process_help_command(message: types.Message):
    await message.answer('''Я умею выполнять такие команды:
    /start - Запустить бота
    /help - Этот текст
    /links - Список ссылок
    /dynamic - Список опций
    ''')

@dp.message(CommandStart())
async def process_start_command(message: types.Message):
    sent_message = await message.answer("🔄 Загружаю список стран...")
    keyboard = await create_letters_menu()
    await sent_message.edit_text(text='🌍 Выберите первую букву названия страны:', reply_markup= keyboard)

@dp.message(Command(commands=['links']))
async def process_links_command(message: types.Message):
    await message.answer(text='Список ссылок', reply_markup= await build_keyboard(url_kbd, is_inline=True, url=True))


@dp.callback_query(LetterCallback.filter())
async def handle_letter_callback(callback: types.CallbackQuery, callback_data: LetterCallback):
    letter = callback_data.letter
    await callback.answer()
    await callback.message.edit_text("🔄 Загружаю страны...")
    keyboard = await create_countries_menu(letter)
    await callback.message.edit_text("🌍 Выберите страну:", reply_markup=keyboard)


@dp.callback_query(BackCallback.filter())
async def handle_back_callback(callback: types.CallbackQuery, callback_data: BackCallback):
    await callback.answer()

    if callback_data.to == "main":
        keyboard = await create_letters_menu()
        if keyboard:
            await callback.message.edit_text(
                "🌍 Выберите первую букву названия страны:",
                reply_markup=keyboard
            )
        else:
            await callback.message.edit_text("❌ Не удалось загрузить главное меню.")




if __name__ == '__main__':
    dp.run_polling(bot)
