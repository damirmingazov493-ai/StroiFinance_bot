import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Загружаем токен
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Создаем бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_name = message.from_user.first_name or "друг"
    await message.answer(f"Привет, {user_name}! Я СтройКазначей. Я помогу тебе не уйти в минус.")

# Обработчик любого другого текста
@dp.message()
async def echo_handler(message: types.Message):
    await message.answer(f"Ты написал: {message.text}. Но я пока умею только здороваться. Нажми /start")

# Запуск
async def main():
    print("Бот запущен... Иди в Телеграм и проверяй!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())