import asyncio
import re
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

TOKEN = "8260895520:AAEzXRAHbTsBrC6RLNsQgpJDfjsE7gpXBRw"

BAD_WORDS = [
    "zaybal", "zybal", "sikaman", "qoto", "qotogim", "q0t0gm", "qotog'im",
    "am", "jalab", "ske", "yibancha", "yiban", "y1ban", 
    "dalbyob", "dalbayob", "suka", "oneniami", "kot", "yebat", "kotmisan"
, "ye gandon", "gandon"]

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(F.text)
async def check_words(message: Message):
    text = message.text
    original_text = text
    
    for word in BAD_WORDS:
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        text = pattern.sub("SO'KINISH SO'Z!", text)

    if text != original_text:
        try:
            await message.delete()
        except Exception:
            pass
        
        user_name = message.from_user.first_name
        await message.answer(f"⚠️ <b>{user_name}</b>, so'kinish taqiqlangan!\n{text}", parse_mode="HTML")

async def main():
    # Eski webhookni o'chirish va ortiqcha xabarlarni tozalash
    await bot.delete_webhook(drop_pending_updates=True)
    print("Bot muvaffaqiyatli ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())