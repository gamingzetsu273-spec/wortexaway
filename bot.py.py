import asyncio
import re
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

# Sizning tokeningiz
TOKEN = "8260895520:AAEzXRAHbTsBrC6RLNsQgpJDfjsE7gpXBRw"

# Taqiqlangan so'zlar ro'yxati
BAD_WORDS = [
    "zaybal", "zybal", "sikaman", "qoto", "qotogim", "q0t0gm", "qotog'im",
    "am", "jalab", "ske", "yibancha", "yiban", "y1ban", 
    "dalbyob", "dalbayob", "suka", "oneniami"
]

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(F.text)
async def filter_bad_words(message: Message):
    text = message.text
    original_text = text
    
    # So'zlarni almashtirish
    for word in BAD_WORDS:
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        text = pattern.sub("SO'KINISH SO'Z!", text)

    # Agar so'z o'zgargan bo'lsa
    if text != original_text:
        try:
            await message.delete()
        except Exception:
            pass
        
        user_name = message.from_user.first_name
        await message.answer(f"<b>{user_name}:</b> {text}", parse_mode="HTML")

async def main():
    print("Bot muvaffaqiyatli ishga tushdi va so'kinishlarni filter qilmoqda...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())