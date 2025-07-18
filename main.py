import os



from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from aiogram.filters.callback_data import CallbackData
from aiohttp import ClientSession

from dotenv import load_dotenv

from kbd import build_keyboard
from utils import set_loglevel, group_countries_by_letter
from api import get_countries_list, get_country_details

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


@dp.callback_query(CountryCallback.filter())
async def handle_country_callback(callback: types.CallbackQuery, callback_data: CountryCallback):
    country_code = callback_data.code

    await callback.answer()
    await callback.message.edit_text("🔄 Загружаю информацию о стране...")

    # Получаем детальную информацию о стране
    async with ClientSession() as session:
        country = await get_country_details(url, session, country_code)
    first_letter = country['name'][0].upper()
    kbd ={LetterCallback(letter=first_letter).pack():f"⬅️ Назад к странам на {first_letter}",
          BackCallback(to="main").pack():"🏠 Главное меню",}
    keyboard = await build_keyboard(kbd, is_inline=True)
    await callback.message.edit_text(
        f"🌍 Название: {country['name']}\n"
        f"🌍 Название на русском: {country['native']}\n"
        f"🌍 Эмодзи: {country['emoji']}\n"
        f"🌍 Валюта: {country['currency']}\n"
        f"🌍 Языки: {', '.join([f'{lang["code"]} - {lang["name"]}' for lang in country['languages']])}",
        reply_markup=keyboard)

if __name__ == '__main__':
    dp.run_polling(bot)
