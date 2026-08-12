import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = "8853682793:AAGuqQaOSu9Ly4KAe2KwmjlMVSgrYLWI0U4"
ALLOWED_USERNAME = "Musilmanchild"
SPAM_TEXT = "Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N Y1B0N"

bot = Bot(token=TOKEN)
dp = Dispatcher()

spam_tasks = {}

@dp.message(Command("start"))
async def start_spam(message: types.Message):
    if message.from_user.username != ALLOWED_USERNAME:
        await message.answer("Bu bot faqat ma'lum bir foydalanuvchi uchun mo'ljallangan.")
        return

    chat_id = message.chat.id
    if chat_id in spam_tasks and not spam_tasks[chat_id].done():
        await message.answer("Spam allaqachon ishlamoqda!")
        return

    await message.answer("🚀 Spam boshlandi...")

    async def send_messages():
        try:
            while True:
                await bot.send_message(chat_id=chat_id, text=SPAM_TEXT)
                # Soniyasiga 5 ta xabar (1 / 5 = 0.2 sekund)
                await asyncio.sleep(0.2)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logging.error(f"Xatolik: {e}")

    spam_tasks[chat_id] = asyncio.create_task(send_messages())

@dp.message(Command("stop"))
async def stop_spam(message: types.Message):
    if message.from_user.username != ALLOWED_USERNAME:
        return

    chat_id = message.chat.id
    if chat_id in spam_tasks and not spam_tasks[chat_id].done():
        spam_tasks[chat_id].cancel()
        await message.answer("🛑 Spam to'xtatildi!")
    else:
        await message.answer("Hozirda faol spam yo'q.")

async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
