# ============================================================
# Group Manager Bot — Blacklist
# Author: Mr. Stark
# ============================================================

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus
from pyrogram import Client, filters, enums
import db
import re
import logging

logger = logging.getLogger(__name__)


async def is_power(client, chat_id: int, user_id: int) -> bool:
    member = await client.get_chat_member(chat_id, user_id)
    return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]


BLACKLIST_HELP_TEXT = (
    f"<blockquote expandable>"
    f"<b>╔══════════════════╗</b>\n"
    f"<b>🚫 ʙʟᴧᴄᴋʟɪsᴛ</b>\n"
    f"<b>╚══════════════════╝</b>\n\n"
    
    f"<b>❖ ᴄᴏᴍᴍᴧɴᴅs ❖</b>\n\n"
    f"<b>➻ /addblack &lt;word&gt; — ᴧᴅᴅ ᴡᴏʀᴅ ᴛᴏ ʙʟᴧᴄᴋʟɪsᴛ</b>\n"
    f"<b>➻ /rmblack &lt;word&gt; — ʀᴇᴍᴏᴠᴇ ғʀᴏᴍ ʙʟᴧᴄᴋʟɪsᴛ</b>\n"
    f"<b>➻ /blacklist — ʟɪsᴛ ᴧʟʟ ʙʟᴧᴄᴋʟɪsᴛᴇᴅ ᴡᴏʀᴅs</b>\n\n"
    
    f"<b>➻ 🌟 ᴋᴇᴇᴘ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴄʟᴇᴧɴ ᴧɴᴅ sᴧғᴇ</b>"
    f"</blockquote>"
)


def register_blacklist_handler(app: Client):

    @app.on_message(filters.group & filters.command("addblack"))
    async def addblack_cmd(client, message: Message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Only admins can use this command.")

        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            return await message.reply_text("⚙️ Usage: <code>/addblack &lt;word&gt;</code>", parse_mode=enums.ParseMode.HTML)

        word = parts[1].strip().lower()
        existing = await db.get_blacklist(message.chat.id)

        if word in existing:
            return await message.reply_text(f"⚠️ <code>{word}</code> is already blacklisted.", parse_mode=enums.ParseMode.HTML)

        await db.add_blacklist_word(message.chat.id, word)
        await message.reply_text(f"✅ Word <code>{word}</code> added to blacklist.", parse_mode=enums.ParseMode.HTML)


    @app.on_message(filters.group & filters.command("rmblack"))
    async def rmblack_cmd(client, message: Message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Only admins can use this command.")

        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            return await message.reply_text("⚙️ Usage: <code>/rmblack &lt;word&gt;</code>", parse_mode=enums.ParseMode.HTML)

        word = parts[1].strip().lower()
        removed = await db.remove_blacklist_word(message.chat.id, word)

        if removed:
            await message.reply_text(f"🗑️ Word <code>{word}</code> removed from blacklist.", parse_mode=enums.ParseMode.HTML)
        else:
            await message.reply_text(f"⚠️ <code>{word}</code> was not in the blacklist.", parse_mode=enums.ParseMode.HTML)


    @app.on_message(filters.group & filters.command("blacklist"))
    async def blacklist_cmd(client, message: Message):
        words = await db.get_blacklist(message.chat.id)

        if not words:
            return await message.reply_text("📭 No blacklisted words in this group.")

        word_list = "\n".join(f"• <code>{w}</code>" for w in sorted(words))
        await message.reply_text(
            f"🚫 <b>Blacklisted Words:</b>\n\n{word_list}",
            parse_mode=enums.ParseMode.HTML
        )


    @app.on_message(filters.group & filters.text & ~filters.service, group=10)
    async def enforce_blacklist(client, message: Message):
        try:
            member = await client.get_chat_member(message.chat.id, message.from_user.id)
            if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                return
        except:
            return

        words = await db.get_blacklist(message.chat.id)
        if not words:
            return

        text_lower = message.text.lower()
        for word in words:
            pattern = re.compile(rf"\b{re.escape(word)}\b", re.IGNORECASE)
            if pattern.search(text_lower):
                try:
                    await message.delete()
                except Exception as e:
                    logger.error(f"Blacklist delete error: {e}")
                return
