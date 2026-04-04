# ============================================================
# Group Manager Bot — Abuse Detection
# Author: Mr. Stark
# ============================================================

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus
import db
import re

# ==========================================================
# Abuse word list — apne hisaab se badha sakte ho
# ==========================================================
ABUSE_WORDS = [
    "bc", "mc", "bkl", "chutiya", "madarchod", "bhenchod",
    "randi", "harami", "kamina", "kutte", "saale", "gaandu", "lauda", "laura", "harami", "bsdk", "bhosdi", "betichod", "maa ka", "bahan ki",
    "lodu", "bhosdike", "chut", "lund", "teri ma", "fuck",
    "bitch", "bastard", "asshole", "motherfucker", "fucker",
    "shit", "cunt", "whore", "slut", "dickhead", "madharxod", "madharchod", "sala", "rand", "mc", "bc", "mkc", "chut", "boor", "bur",
]

# Pattern — pure word match, case insensitive
ABUSE_PATTERN = re.compile(
    r"\b(" + "|".join(re.escape(w) for w in ABUSE_WORDS) + r")\b",
    re.IGNORECASE
)


async def is_power(client, chat_id: int, user_id: int) -> bool:
    member = await client.get_chat_member(chat_id, user_id)
    return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]


def register_abuse_handler(app: Client):

    # ==========================================================
    # /noabuse on/off — Toggle abuse detection
    # ==========================================================

    @app.on_message(filters.group & filters.command("noabuse"))
    async def noabuse_toggle(client, message: Message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Only the administrator can use this command..")

        parts = message.text.split(maxsplit=1)
        if len(parts) < 2 or parts[1].lower() not in ["on", "off"]:
            status = await db.get_abuse_status(message.chat.id)
            current = "🟢 ON" if status else "🔴 OFF"
            return await message.reply_text(
                f"⚙️ Usage: `/noabuse on` ya `/noabuse off`\n\n"
                f"📊 Current Status: {current}"
            )

        status = parts[1].lower() == "on"
        await db.set_abuse_status(message.chat.id, status)

        if status:
            await message.reply_text(
                "✅ **Abuse Detection ON!**\n\n"
                " 💯 Now the message of the person abusing will be deleted. "
            )
        else:
            await message.reply_text(
                "⚠️ **Abuse Detection OFF!**\n\n"
                "Abuse filter turned off."
            )

    # ==========================================================
    # Enforce — incoming messages check karo
    # ==========================================================

    @app.on_message(filters.group & filters.text & ~filters.service, group=2)
    async def enforce_abuse(client, message: Message):
        try:
            member = await client.get_chat_member(message.chat.id, message.from_user.id)
            if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                return
        except:
            return

        abuse_on = await db.get_abuse_status(message.chat.id)
        if not abuse_on:
            return

        if message.text and ABUSE_PATTERN.search(message.text):
            try:
                await message.delete()
                warn_msg = await client.send_message(
                    message.chat.id,
                    f"⚠️ {message.from_user.mention}, Abusing is not allowed! The message has been deleted. 🚫"
                )
                # 5 second baad warn msg bhi delete karo (optional clean look)
                import asyncio
                await asyncio.sleep(5)
                await warn_msg.delete()
            except Exception:
                pass
