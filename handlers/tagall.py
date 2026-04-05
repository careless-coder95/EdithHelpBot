# ============================================================
# Group Manager Bot — Tag All
# Author: Mr. Stark
# ============================================================

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus, ChatMembersFilter
import asyncio
import logging

logger = logging.getLogger(__name__)

# Track which chats have active tagging — to handle /stop
_active_tagging: set = set()


async def is_power(client, chat_id: int, user_id: int) -> bool:
    member = await client.get_chat_member(chat_id, user_id)
    return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]


# ==========================================================
# Help Text
# ==========================================================

TAGALL_HELP_TEXT = """
╔════════════════════════╗
   📢 TAG ALL – MENTION MEMBERS
╚════════════════════════╝

🛠️ How to use:

• /tagall
  → Mention all group members.

• /tagall <message>
  → Mention all members with
    a custom message.

• /stop
  → Stop tagging immediately.

👮 Permissions:
- Only admins can use this command.
- Bot must be admin in the group.

⚠️ Note:
- Members are mentioned in batches
  of 5 to avoid Telegram rate limits.
- Deleted accounts are skipped.
"""


def register_tagall_handler(app: Client):

    # ==========================================================
    # /tagall
    # ==========================================================

    @app.on_message(filters.group & filters.command("tagall"))
    async def tagall_cmd(client, message: Message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Only admins can use this command.")

        chat_id = message.chat.id

        if chat_id in _active_tagging:
            return await message.reply_text("⚠️ Tagging is already in progress. Use `/stop` to stop it.")

        parts = message.text.split(maxsplit=1)
        custom_msg = parts[1] if len(parts) > 1 else ""

        _active_tagging.add(chat_id)

        header = f"📢 **{custom_msg}**\n\n" if custom_msg else "📢 **Attention everyone!**\n\n"

        try:
            batch = []
            batch_num = 0

            async for member in client.get_chat_members(chat_id):
                # Skip bots, deleted accounts and anonymous admins
                if member.user.is_bot or member.user.is_deleted:
                    continue

                if chat_id not in _active_tagging:
                    await client.send_message(chat_id, "🛑 Tagging stopped.")
                    return

                batch.append(member.user.mention)

                # Send in batches of 5
                if len(batch) == 5:
                    batch_num += 1
                    await client.send_message(
                        chat_id,
                        header + " ".join(batch)
                    )
                    batch.clear()
                    await asyncio.sleep(2)  # Avoid rate limit

            # Send remaining members
            if batch and chat_id in _active_tagging:
                await client.send_message(
                    chat_id,
                    header + " ".join(batch)
                )

        except Exception as e:
            logger.error(f"Tagall error: {e}")
            await client.send_message(chat_id, f"❌ Tagging failed: {e}")
        finally:
            _active_tagging.discard(chat_id)


    # ==========================================================
    # /stop — Stop active tagging
    # ==========================================================

    @app.on_message(filters.group & filters.command("stop"))
    async def stop_cmd(client, message: Message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Only admins can use this command.")

        chat_id = message.chat.id

        if chat_id in _active_tagging:
            _active_tagging.discard(chat_id)
            await message.reply_text("🛑 Tagging has been stopped.")
        else:
            await message.reply_text("⚠️ No active tagging in progress.")
