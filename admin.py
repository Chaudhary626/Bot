from aiogram import types
from config import ADMIN_IDS
from database import db_query, db_query as dq
from datetime import datetime

def is_admin(user_id):
    r = dq("SELECT is_admin FROM users WHERE user_id=?", (user_id,), one=True)
    return (user_id in ADMIN_IDS) or (r and r[0])

async def admin_dashboard(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.reply("⛔ Only admin can access the dashboard.")
        return
    users = dq("SELECT user_id, username, warnings, status, blocked FROM users")
    total_users = len(users)
    blocked = sum(1 for u in users if u[4])
    active_pairings = dq("SELECT COUNT(*) FROM users WHERE status != 'idle'", (), one=True)[0]
    total_proofs = dq("SELECT COUNT(*) FROM proofs", (), one=True)[0]
    await message.answer(
        f"🛠 *Admin Dashboard*\n\n"
        f"👥 Total users: {total_users}\n"
        f"🛑 Blocked: {blocked}\n"
        f"🔄 Active pairings: {active_pairings}\n"
        f"📤 Proofs: {total_proofs}\n"
        f"\nUse /users, /proofs, /block, /unblock, /resetwarnings, /approveproof, /rejectproof, /notify, /export, /addadmin, /removeadmin"
    )

async def admin_users(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.reply("⛔ Only admin can access.")
        return
    users = dq("SELECT user_id, username, warnings, status, blocked FROM users")
    msg = "👥 *Users List:*\n"
    for u in users:
        block = "❌" if u[4] else "✅"
        msg += f"{u[1]} (ID: {u[0]}) — Warn: {u[2]}, Stat: {u[3]}, {block}\n"
    await message.answer(msg)

async def admin_block(message: types.Message, user_id):
    dq("UPDATE users SET blocked=1 WHERE user_id=?", (user_id,), commit=True)
    dq("INSERT INTO logs (admin_id, action, target_user, at) VALUES (?,?,?,?)",
        (message.from_user.id, "block", user_id, datetime.utcnow()), commit=True)
    await message.answer(f"User {user_id} blocked.")

async def admin_unblock(message: types.Message, user_id):
    dq("UPDATE users SET blocked=0 WHERE user_id=?", (user_id,), commit=True)
    dq("INSERT INTO logs (admin_id, action, target_user, at) VALUES (?,?,?,?)",
        (message.from_user.id, "unblock", user_id, datetime.utcnow()), commit=True)
    await message.answer(f"User {user_id} unblocked.")
# ...similarly for resetwarnings, approveproof, rejectproof, notify, export, addadmin, removeadmin