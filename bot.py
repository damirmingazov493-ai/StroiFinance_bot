import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from supabase import create_client, Client

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Подключаем базу данных
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_name = message.from_user.first_name or "друг"
    await message.answer(
        f"Привет, {user_name}! Я СтройКазначей. 🤖\n\n"
        "Я умею считать твои деньги. Просто напиши мне:\n"
        "👉 **Расход 50000 цемент**\n"
        "👉 **Доход 100000 аванс**\n\n"
        "А чтобы узнать баланс, напиши /balance"
    )

@dp.message(Command("balance"))
async def cmd_balance(message: types.Message):
    user_id = message.from_user.id
    
    # Достаем все транзакции пользователя из базы
    response = supabase.table("transactions").select("*").eq("user_id", user_id).execute()
    
    income = 0
    expense = 0
    
    for row in response.data:
        if row['type'] == 'income':
            income += row['amount']
        elif row['type'] == 'expense':
            expense += row['amount']
            
    balance = income - expense
    
    await message.answer(
        f"📊 **Твой финансовый отчет:**\n\n"
        f"🟢 Доходы: {income:,.2f} ₽\n"
        f"🔴 Расходы: {expense:,.2f} ₽\n"
        f"💰 **Баланс: {balance:,.2f} ₽**"
    )

@dp.message()
async def handle_transaction(message: types.Message):
    text = message.text.strip()
    parts = text.split(maxsplit=2) 
    
    if len(parts) < 2 or parts[0].lower() not in ['расход', 'доход']:
        await message.answer("Я не понял. Напиши в формате:\n`Расход 5000 цемент` или `Доход 10000 аванс`")
        return

    type_word = parts[0].lower()
    tx_type = 'expense' if type_word == 'расход' else 'income'
    
    try:
        amount = float(parts[1].replace(',', '.'))
    except ValueError:
        await message.answer("Сумма должна быть числом. Например: Расход 5000 бетон")
        return
        
    description = parts[2] if len(parts) > 2 else "Без описания"

    # Сохраняем в Supabase
    supabase.table("transactions").insert({
        "user_id": message.from_user.id,
        "amount": amount,
        "type": tx_type,
        "description": description
    }).execute()

    if tx_type == 'expense':
        await message.answer(f"✅ Записал расход: **{amount:,.2f} ₽** на '{description}'")
    else:
        await message.answer(f"✅ Записал доход: **{amount:,.2f} ₽** от '{description}'")

async def main():
    print("Бот запущен... Иди в Телеграм и проверяй!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())