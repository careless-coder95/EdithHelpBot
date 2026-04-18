# ============================================================
# Group Manager Bot — Language System
# Author: Mr. Stark
# ============================================================

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus
from languages import LANGUAGE_NAMES
import db
import logging

logger = logging.getLogger(__name__)


async def is_power(client, chat_id: int, user_id: int) -> bool:
    member = await client.get_chat_member(chat_id, user_id)
    return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]


LANGUAGE_HELP_TEXT = (
    "╔══════════════════╗\n"
    "   🌍 LANGUAGE SYSTEM\n"
    "╚══════════════════╝\n\n"
    "<b>Commands:</b>\n\n"
    "• /setlang &lt;code&gt; — Set group language\n"
    "• /langlist — Show all available languages\n\n"
    "<b>Available Languages:</b>\n"
    "🇬🇧 <code>en</code> — English\n"
    "🇮🇳 <code>hi</code> — Hindi\n"
    "🇸🇦 <code>ar</code> — Arabic\n"
    "🇪🇸 <code>es</code> — Spanish\n"
    "🇫🇷 <code>fr</code> — French\n"
    "🇷🇺 <code>ru</code> — Russian\n"
    "🇩🇪 <code>de</code> — German\n"
    "🇵🇹 <code>pt</code> — Portuguese\n"
    "🇮🇩 <code>id</code> — Indonesian\n"
    "🇹🇷 <code>tr</code> — Turkish\n\n"
    "<i>Example: /setlang hi</i>"
)


def register_language_handler(app: Client):

    @app.on_message(filters.group & filters.command("setlang"))
    async def setlang_cmd(client, message: Message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text(
                "❌ Only admins can use this command.",
                parse_mode="html"
            )

        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            current = await db.get_group_lang(message.chat.id)
            return await message.reply_text(
                f"⚙️ Usage: <code>/setlang &lt;code&gt;</code>\n\n"
                f"📊 Current: <code>{current}</code>\n\n"
                f"Use /langlist to see all options.",
                parse_mode="html"
            )

        code = parts[1].strip().lower()
        if code not in LANGUAGE_NAMES:
            langs = " | ".join(f"<code>{k}</code>" for k in LANGUAGE_NAMES)
            return await message.reply_text(
                f"⚠️ Invalid language code!\n\nAvailable: {langs}",
                parse_mode="html"
            )

        await db.set_group_lang(message.chat.id, code)
        await message.reply_text(
            f"✅ Language set to <b>{LANGUAGE_NAMES[code]}</b>!",
            parse_mode="html"
        )

    @app.on_message(filters.group & filters.command("langlist"))
    async def langlist_cmd(client, message: Message):
        current = await db.get_group_lang(message.chat.id)
        lines = "\n".join(
            f"{'✅' if k == current else '•'} {v} — <code>{k}</code>"
            for k, v in LANGUAGE_NAMES.items()
        )
        await message.reply_text(
            f"🌍 <b>Available Languages:</b>\n\n{lines}\n\n"
            f"<i>Use /setlang &lt;code&gt; to change.</i>",
            parse_mode="html"
        )
