import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

# ЗАМЕНИ НА СВОЙ ТОКЕН ОТ @BotFather
BOT_TOKEN = "ВСТАВЬ_СЮДА_ТОКЕН"

# ЗАМЕНИ ПОСЛЕ ДЕПЛОЯ НА RENDER
WEBAPP_URL = "https://westy-toon.onrender.com"

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

@dp.message()
async def start(msg: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Открыть WESTY TOON", web_app=WebAppInfo(url=WEBAPP_URL))]
    ])
    await msg.answer("WESTY TOON — твой личный адресник. Нажми кнопку ниже:", reply_markup=kb)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())