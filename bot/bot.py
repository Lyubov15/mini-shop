import asyncio
import os
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import httpx
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BACKEND_URL = "http://127.0.0.1:8000"
ADMIN_ID = 1840919755

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    # Наша ссылка из Ngrok
    web_app_url = "https://overdress-preorder-scrambled.ngrok-free.dev"
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛍 Открыть каталог", web_app=WebAppInfo(url=web_app_url))]
    ])
    await message.answer("Привет. У меня есть товар", reply_markup=kb)

@dp.message(F.photo & F.caption)
async def handle_new_product(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("У вас нет прав для создания товара.")
        return

    name = message.caption.strip()
    photo = message.photo[-1]
    
    print(f"--- ПОЛУЧЕНО ФОТО: {name} ---")
    await message.answer("Загружаю товар, подождите...")

    try:
        print("Скачиваю файл из Telegram...")
        file = await bot.get_file(photo.file_id)
        file_bytes = await bot.download_file(file.file_path)
        print(f"Файл скачан, размер: {len(file_bytes.getvalue())} байт")

        print("Отправляю на бэкенд...")
        async with httpx.AsyncClient() as client:
            files = {"photo": ("photo.jpg", file_bytes.getvalue(), "image/jpeg")}
            data = {"name": name}
            response = await client.post(f"{BACKEND_URL}/admin/products", files=files, data=data)
            
            print(f"4. Ответ от бэкенда: {response.status_code}")
            if response.status_code == 200:
                await message.answer(f"✅ Товар «{name}» успешно создан!")
            else:
                print(f"Ошибка: {response.text}")
                await message.answer(f"❌ Ошибка сервера: {response.text}")
    except Exception as e:
        print(f"!!! ИСКЛЮЧЕНИЕ: {e}")
        await message.answer(f"❌ Ошибка: {e}")
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())