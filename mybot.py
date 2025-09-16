from aiogram import Bot, Dispatcher, executor, types

# ----- بياناتك -----
API_TOKEN = "7087558723:AAEAVJvaxNFH4EthjnTpt9jm5pCv8AnQ-Cs"  # توكن البوت
API_ID = 28146956   # API ID من my.telegram.org
API_HASH = "b956d1ba04889e627941312b6d842711"  # API Hash من my.telegram.org
# ------------------

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# نخزن اليوزر مؤقت هنا
user_to_hunt = {}

# --- الكيبورد الرئيسي ---
def main_keyboard():
    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton("Run A", callback_data="run_a"),
        types.InlineKeyboardButton("Run B", callback_data="run_b")
    )
    kb.add(
        types.InlineKeyboardButton("➕ إضافة سيشن", callback_data="add_session"),
        types.InlineKeyboardButton("📜 عرض الجلسات", callback_data="list_sessions")
    )
    kb.add(
        types.InlineKeyboardButton("🗑️ حذف جلسة", callback_data="delete_session"),
        types.InlineKeyboardButton("⛔ إيقاف البوت", callback_data="stop_bot")
    )
    kb.add(
        types.InlineKeyboardButton("👤 User", callback_data="set_user")
    )
    return kb

# --- start command ---
@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await message.answer("أهلاً بك! اختر أحد الأزرار:", reply_markup=main_keyboard())

# --- زر User ---
@dp.callback_query_handler(lambda c: c.data == "set_user")
async def process_set_user(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "قم بإرسال اليوزر الذي تريد تثبيت عليه (مثال: @username)")
    await bot.answer_callback_query(callback_query.id)

# --- التقاط اليوزر ---
@dp.message_handler(lambda message: message.text.startswith("@"))
async def save_user(message: types.Message):
    user_to_hunt[message.from_user.id] = message.text
    await message.reply(f"✅ تم حفظ اليوزر: {message.text}\nالآن اختر Run A أو Run B للبدء.")

# --- Run A ---
@dp.callback_query_handler(lambda c: c.data == "run_a")
async def run_a(callback_query: types.CallbackQuery):
    uid = callback_query.from_user.id
    if uid not in user_to_hunt:
        await bot.send_message(uid, "❌ لم تقم بتحديد يوزر بعد! اضغط على زر User أولاً.")
    else:
        username = user_to_hunt[uid]
        await bot.send_message(uid, f"🚀 تم تشغيل Run A على {username} (يثبت على يوزر ويخلي بالقناة إذا متاح).")
    await bot.answer_callback_query(callback_query.id)

# --- Run B ---
@dp.callback_query_handler(lambda c: c.data == "run_b")
async def run_b(callback_query: types.CallbackQuery):
    uid = callback_query.from_user.id
    if uid not in user_to_hunt:
        await bot.send_message(uid, "❌ لم تقم بتحديد يوزر بعد! اضغط على زر User أولاً.")
    else:
        username = user_to_hunt[uid]
        await bot.send_message(uid, f"🚀 تم تشغيل Run B على {username} (يثبت على الحساب إذا متاح).")
    await bot.answer_callback_query(callback_query.id)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
