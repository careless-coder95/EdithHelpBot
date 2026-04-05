# ============================================================
# Group Manager Bot — Zombie Remover
# Author: Mr. Stark
# ============================================================

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus
import logging

logger = logging.getLogger(__name__)


async def is_power(client, chat_id: int, user_id: int) -> bool:
    member = await client.get_chat_member(chat_id, user_id)
    return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]


# ==========================================================
# Help Text
# ==========================================================

ZOMBIE_HELP_TEXT = """
╔════════════════════╗
   ⚠️ REMOVE DELETED ACCOUNTS
╚════════════════════╝

🛠️ Commands:

• /zombie
  → Scan and remove all deleted
    accounts from the group instantly.

ℹ️ Notes:
- Bot must be admin with ban permission.
- Only admins can use this command.
- All deleted Telegram accounts will
  be removed immediately.
"""


def register_zombie_handler(app: Client):

    # ==========================================================
    # /zombie — Scan and remove deleted accounts
    # ==========================================================

    @app.on_message(filters.group & filters.command("zombie"))
    async def zombie_cmd(client, message: Message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Only admins can use this command.")

        scanning = await message.reply_text("🔍 Scanning for deleted accounts...")

        removed = 0
        failed = 0

        async for member in client.get_chat_members(message.chat.id):
            if member.user.is_deleted:
                try:
                    await client.ban_chat_member(message.chat.id, member.user.id)
                    await client.unban_chat_member(message.chat.id, member.user.id)
                    removed += 1
                except Exception as e:
                    logger.error(f"Zombie remove error: {e}")
                    failed += 1

        if removed == 0:
            await scanning.edit_text("✅ No deleted accounts found in this group.")
        else:
            await scanning.edit_text(
                f"✅ **Zombie Scan Complete!**\n\n"
                f"🗑️ Removed: `{removed}` deleted accounts\n"
                f"❌ Failed: `{failed}`"
            )
