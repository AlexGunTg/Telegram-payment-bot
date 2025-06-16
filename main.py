from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
import logging
import os

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
print(f"BOT_TOKEN: {BOT_TOKEN}")  # Отладка

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Кнопки оплаты
start_kb = ReplyKeyboardMarkup(resize_keyboard=True)
start_kb.add(KeyboardButton("💳 Оплата"))

currency_kb = ReplyKeyboardMarkup(resize_keyboard=True)
currency_kb.row("Рубли", "PayPal").row("Евро", "Доллар").row("Гривна", "USDT в Binance").add("⬅️ Назад")

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    text = ("Здравствуйте, меня зовут Александр Гунько.\n"
            "Я массажист-реабилитолог, преподаватель хатха-йоги и ведущий каналов «Анатомия и Биомеханика».\n"
            "Нажмите кнопку «Оплата», чтобы получить реквизиты.")
    await message.answer(text, reply_markup=start_kb)

@dp.message_handler(lambda message: message.text == "💳 Оплата")
async def payment_options(message: types.Message):
    await message.answer("Выберите удобный способ оплаты:", reply_markup=currency_kb)

@dp.message_handler(lambda message: message.text == "⬅️ Назад")
async def back_to_start(message: types.Message):
    await send_welcome(message)

@dp.message_handler(lambda message: message.text in ["Рубли", "PayPal", "Евро", "Доллар", "Гривна", "USDT в Binance"])
async def send_payment_details(message: types.Message):
    text = {
        "Рубли": "Карта Тинькофф: 5536 9140 8865 7683",
        "PayPal": "PayPal: jivoemilo@gmail.com",
        "Евро": ("IBAN: GB48CLJU00997186505114\n"
                 "Карта: 5375 4199 0916 1356\n"
                 "Имя: HUNKO OLEKSANDR\n"
                 "Банк: 15 Kingsway, London WC2B 6UN"),
        "Доллар": ("IBAN: UA713220010000026202333147176\n"
                   "Карта: 5375 4188 1395 9798\n"
                   "Имя: HUNKO OLEKSANDR\n"
                   "Банк: 15 Kingsway, London WC2B 6UN"),
        "Гривна": "Карта Монобанк: 4441 1114 0091 0463",
        "USDT в Binance": ("Кошелёк: TWMVgvk1nx3QCWVnZrZvh4w8EPLH5XbynE\n"
                           "Сеть: Tron (TRC20)")
    }[message.text]
    await message.answer(text + "\n\nПосле оплаты отправьте сюда скриншот или фото чека.")

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_receipt(message: types.Message):
    admin_username = ADMIN_USERNAME
    caption = f"💰 Новый платёж от @{message.from_user.username or message.from_user.id}"
    await bot.send_photo(chat_id=admin_username, photo=message.photo[-1].file_id, caption=caption)
    await message.answer("Спасибо! Ваш чек отправлен на проверку. Мы свяжемся с вами в ближайшее время.")

@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def handle_document_receipt(message: types.Message):
    admin_username = ADMIN_USERNAME
    file_id = message.document.file_id
    caption = f"📎 Новый файл от @{message.from_user.username or message.from_user.id}"
    await bot.send_document(chat_id=admin_username, document=file_id, caption=caption)
    await message.answer("Файл получен. Спасибо! Мы свяжемся с вами после проверки.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
