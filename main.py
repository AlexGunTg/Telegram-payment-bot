from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import logging
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Кнопки оплаты
start_kb = ReplyKeyboardMarkup(resize_keyboard=True)
start_kb.add(KeyboardButton("💳 Оплата"))

currency_kb = ReplyKeyboardMarkup(resize_keyboard=True)
currency_kb.row("Рубль", "PayPal", "Евро", "Доллар").row("Гривна", "USDT в Binance").add("🔙 Назад")

@dp.message(commands=["start"])
async def send_welcome(message: types.Message):
    text = (
        "Здравствуйте, меня зовут Александр Гунько.\n"
        "Я массажист-реабилитолог, преподаватель хатха-йоги и ведущий каналов «Анатомия и Биомеханика».\n"
        "Нажмите кнопку «Оплата», чтобы получить реквизиты."
    )
    await message.answer(text, reply_markup=start_kb)

@dp.message(lambda message: message.text == "💳 Оплата")
async def payment_options(message: types.Message):
    await message.answer("Выберите удобный способ оплаты:", reply_markup=currency_kb)

@dp.message(lambda message: message.text == "🔙 Назад")
async def back_to_start(message: types.Message):
    await send_welcome(message)

@dp.message(lambda message: message.text in ["Рубль", "PayPal", "Евро", "Доллар", "Гривна", "USDT в Binance"])
async def send_payment_details(message: types.Message):
    text = (
        "Реквизиты:\n"
        "Рубль: Карта Тинькофф: 5536 9140 8865 7683\n"
        "PayPal: jivoemilol@gmail.com\n"
        "Евро: IBAN: GB48CLJU00997186505114\n"
        "Карта: 5375 4195 0916 1136\n"
        "Имя: HUNKO OLEKSANDR\n"
        "Банк: 15 Kingsway, London WC2B 6UN\n"
        "Доллар: IBAN: UA7132200100000260233414716\n"
        "Карта: 5375 4188 1395 9798\n"
        "Имя: HUNKO OLEKSANDR\n"
        "Банк: 15 Kingsway, London WC2B 6UN\n"
        "Гривна: Карта Монобанк: 4441 1114 0091 0463\n"
        "USDT в Binance: Кошелёк: TMWKyhk13XCqWvnZrZh4w8EPLH5XbyneY\n"
        "Сеть: Tron (TRC20)"
    )
    await message.answer(text + "\n\nПосле оплаты отправьте сюда скриншот или фото чека.")

@dp.message(content_types=types.ContentType.PHOTO)
async def handle_receipt(message: types.Message):
    caption = f"Новый платёж от @{message.from_user.username or message.from_user.id}"
    await bot.send_photo(chat_id=ADMIN_USERNAME, photo=message.photo[-1].file_id, caption=caption)
    await message.answer("Спасибо! Ваш чек отправлен на проверку. Мы свяжемся с вами в ближайшее время.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
