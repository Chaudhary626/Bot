from aiogram import types
from database import db_query, add_user

async def handle_start(message: types.Message):
    add_user(message.from_user.id, message.from_user.username or "")
    # ...send welcome_text

async def handle_profile(message: types.Message):
    p = db_query("SELECT username, video_link, warnings, status, blocked FROM users WHERE user_id=?", (message.from_user.id,), one=True)
    if p:
        blocked = "❌ Blocked" if p[4] else "✅ Active"
        await message.answer(
            f"👤 *Profile:*\nUsername: `{p[0]}`\nVideo: {p[1] or '-'}\nWarnings: *{p[2]}*\nStatus: `{p[3]}`\n{blocked}",
            parse_mode="Markdown"
        )
    else:
        await message.answer("Profile not found. Please /start.")

async def handle_history(message: types.Message):
    proofs = db_query("SELECT proof_file, proof_type, submitted_at, verified, rejected FROM proofs WHERE from_user=? ORDER BY submitted_at DESC LIMIT 10", (message.from_user.id,))
    if not proofs:
        await message.answer("Aapne abhi tak koi proof submit nahi kiya.")
        return
    msg = "🕓 *Aapki Last 10 Activities:*\n"
    for pf in proofs:
        status = "✅ Verified" if pf[3] else ("❌ Rejected" if pf[4] else "⏳ Pending")
        msg += f"- [{pf[1]}] at {pf[2][:16]} — {status}\n"
    await message.answer(msg, parse_mode="Markdown")