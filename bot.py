import asyncio
import re
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

TOKEN = "8260895520:AAEzXRAHbTsBrC6RLNsQgpJDfjsE7gpXBRw"

BAD_WORDS = [
    "zaybal", "zybal", "sikaman", "qoto", "qotogim", "q0t0gm", "qotog'im",
    "am", "jalab", "ske", "yibancha", "yiban", "y1ban", 
    "dalbyob", "dalbayob", "suka", "oneniami"
]

bot = Bot(token=TOKEN)
dp = Dispatcher()

class ContestState(StatesGroup):
    waiting_for_amount = State()

# Tugmalar bold qilib qilindi
def get_games_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎮 PUBG Mobile 🎮", callback_data="game_pubg")],
            [InlineKeyboardButton(text="🎯 Counter Strike 2 🎯", callback_data="game_cs2")],
            [InlineKeyboardButton(text="⛏️ Minecraft ⛏️", callback_data="game_mc")],
            [InlineKeyboardButton(text="❌ Qaytish ❌", callback_data="cancel_contest")]
        ]
    )

@dp.message(F.text == "/konkurs")
async def start_contest(message: Message):
    user_name = message.from_user.first_name
    text = f"👤 <b>{user_name}</b>\n\n<b>KONKURSGA START BERISH UCHUN /start DEB YOZING!</b>"
    await message.answer(text, parse_mode="HTML", reply_markup=get_games_keyboard())

@dp.callback_query(F.data.startswith("game_"))
async def select_game(callback: CallbackQuery, state: FSMContext):
    game = callback.data.split("_")[1]
    
    if game == "pubg":
        currency = "UC"
        game_title = "PUBG Mobile"
    elif game == "cs2":
        currency = "CS2 Valyutasi / Skin"
        game_title = "Counter Strike 2"
    elif game == "mc":
        currency = "Minecraft Resursi / Item"
        game_title = "Minecraft"
    else:
        return

    await state.update_data(game_title=game_title, currency=currency)
    await state.set_state(ContestState.waiting_for_amount)
    
    await callback.message.edit_text(
        f"🏆 <b>{game_title}</b> uchun tanlandi!\n\n"
        f"📝 <b>{currency}</b> miqdorini yozing!\n\n"
        f"⚠️ <i>ASOSIYSI AGAR 2TA YOKI 2TADAN KOP ODAM YOZMASA KONKURS BEKOR!❌</i>",
        parse_mode="HTML"
    )
    await callback.answer()

@dp.message(ContestState.waiting_for_amount)
async def receive_amount(message: Message, state: FSMContext):
    data = await state.get_data()
    game_title = data.get("game_title")
    currency = data.get("currency")
    amount = message.text

    await message.answer(
        f"✅ <b>{game_title}</b> konkursi muvaffaqiyatli yaratildi!\n\n"
        f"💰 Miqdor: <b>{amount} {currency}</b>\n"
        f"⚠️ <i>Agar 2 tadan kam odam qatnashsa, konkurs bekor qilinadi!❌</i>",
        parse_mode="HTML"
    )
    await state.clear()

@dp.callback_query(F.data == "cancel_contest")
async def cancel_contest(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("❌ <b>Konkurs jarayoni bekor qilindi.</b>", parse_mode="HTML")
    await callback.answer()

@dp.message(F.text)
async def filter_bad_words(message: Message):
    if not message.text:
        return
        
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
    await bot.delete_webhook(drop_pending_updates=True)
    print("Bot muvaffaqiyatli ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())