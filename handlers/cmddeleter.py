# ============================================================
# Group Manager Bot — Command Deleter
# Author: Mr. Stark
# ============================================================

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus
import db
import re
import logging

logger = logging.getLogger(__name__)


async def is_power(client, chat_id: int, user_id: int) -> bool:
    member = await client.get_chat_member(chat_id, user_id)
    return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]


# Command pattern — /, !, . se shuru hone wale
CMD_PATTERN = re.compile(r"^[/!.]")


# ==========================================================
# Help Text
# ==========================================================

CMDDELETER_HELP_TEXT = """
╔══════════════════╗
   🗑️ CMD DELETER
╚══════════════════╝

Commands jo / ! . se shuru hoti hain
wo automatically delete ho jaati hain.

🔧 Commands:

• /cmd on  — Auto delete ON ✅
• /cmd off — Auto delete OFF ❌

Kaise kaam karta hai:
- Koi bhi /command, !command
  ya .command type kare —
  message turant delete ho jaata hai.
- Admins ki commands delete
  nahi hoti.

👮 Sirf admin configure kar sakta hai.
"""


def register_cmddeleter_handler(app: Client):

    # ==========================================================
    # /cmd on/off
    # ==========================================================

    @app.on_message(filters.group & filters.command("cmd"))
    async def cmd_toggle(client, message: Message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Sirf admin yeh command use kar sakta hai.")

        parts = message.text.split(maxsplit=1)
        if len(parts) < 2 or parts[1].lower() not in ["on", "off"]:
            status = await db.get_cmddeleter_status(message.chat.id)
            current = "🟢 ON" if status else "🔴 OFF"
            return await message.reply_text(
                f"⚙️ Usage: `/cmd on` ya `/cmd off`\n\n📊 Current: {current}"
            )

        status = parts[1].lower() == "on"
        await db.set_cmddeleter_status(message.chat.id, status)

        if status:
            await message.reply_text(
                "✅ **Command Deleter ON!**\n\n"
                "Ab / ! . se shuru hone wali commands automatically delete hongi."
            )
        else:
            await message.reply_text("⚠️ **Command Deleter OFF!**")


    # ==========================================================
    # Enforce — commands detect karke delete karo
    # ==========================================================

    @app.on_message(filters.group & filters.text & ~filters.service, group=7)
    async def enforce_cmddeleter(client, message: Message):
        try:
            member = await client.get_chat_member(message.chat.id, message.from_user.id)
            if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                return
        except:
            return

        if not await db.get_cmddeleter_status(message.chat.id):
            return

        if message.text and CMD_PATTERN.match(message.text):
            try:
                await message.delete()
            except Exception as e:
                logger.error(f"Cmd deleter error: {e}")
