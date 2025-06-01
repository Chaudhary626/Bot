import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from config import API_TOKEN
from database import init_db
from messages import WELCOME_TEXT, HELP_TEXT, CONTACT_TEXT
from user import handle_start, handle_profile, handle_history
from admin import admin_dashboard, admin_users, admin_block, admin_unblock
from proofs import save_proof

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def _(message: types.Message):
    await handle_start(message)

@dp.message_handler(commands=['help'])
async def _(message: types.Message):
    await message.answer(HELP_TEXT, parse_mode="Markdown")

@dp.message_handler(commands=['profile'])
async def _(message: types.Message):
    await handle_profile(message)

@dp.message_handler(commands=['warnings'])
async def _(message: types.Message):
    # ...call warnings function

@dp.message_handler(commands=['history'])
async def _(message: types.Message):
    await handle_history(message)

@dp.message_handler(commands=['contact'])
async def _(message: types.Message):
    await message.answer(CONTACT_TEXT, parse_mode="Markdown")

@dp.message_handler(commands=['dashboard'])
async def _(message: types.Message):
    await admin_dashboard(message)

@dp.message_handler(commands=['users'])
async def _(message: types.Message):
    await admin_users(message)

@dp.message_handler(lambda m: m.text and m.text.startswith("/block"))
async def _(message: types.Message):
    try:
        user_id = int(message.text.split()[1])
        await admin_block(message, user_id)
    except Exception:
        await message.answer("Usage: /block <user_id>")

# ...similarly handlers for /unblock, /resetwarnings, /approveproof, /rejectproof, /notify, /export, /addadmin, /removeadmin

# For proof: accept video/photo
@dp.message_handler(content_types=[types.ContentType.VIDEO, types.ContentType.PHOTO])
async def handle_proof(message: types.Message):
    user_id = message.from_user.id
    # pairing logic, get pair_id
    pair_id = ... # pairing logic
    proof_type = "video" if message.video else "image"
    file_id = message.video.file_id if message.video else message.photo[-1].file_id
    save_proof(user_id, pair_id, file_id, proof_type)
    await message.answer("✅ Proof submit ho gaya.")

if __name__ == "__main__":
    init_db()
    executor.start_polling(dp, skip_updates=True)
