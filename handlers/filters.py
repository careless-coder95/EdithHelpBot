# ============================================================
# Group Manager Bot — Filters (Auto Reply)
# Author: Mr. Stark
# ============================================================

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus
import db
import logging

logger = logging.getLogger(__name__)


async def is_power(client, chat_id: int, user_id: int) -> bool:
    member = await client.get_chat_member(chat_id, user_id)
    return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]


FILTERS_HELP_TEXT = (
    "╔══════════════════╗\n"
    "   📝 FILTERS\n"
    "╚══════════════════╝\n\n"
    "<b>Commands:</b>\n\n"
    "• /filter &lt;keyword&gt;\n"
    "  Reply to a message/sticker to set\n"
    "  auto-reply for that keyword.\n\n"
    "• /stopfilter &lt;keyword&gt;\n"
    "  Remove a filter.\n\n"
    "• /filters\n"
    "  List all active filters.\n\n"
    "🌟 Automate replies and make your\n"
    "group more interactive."
)


def register_filters_handler(app: Client):

    # ==========================================================
    # /filter <keyword> — reply to message to set filter
    # ==========================================================

    @app.on_message(filters.group & filters.command("filter"))
    async def filter_cmd(client, message: Message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Only admins can use this command.")

        if not message.reply_to_message:
            return await message.reply_text(
                "⚙️ Reply to a message or sticker and use:\n"
                "<code>/filter &lt;keyword&gt;</code>",
                parse_mode="html"
            )

        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            return await message.reply_text(
                "⚙️ Usage: Reply to a message and type <code>/filter &lt;keyword&gt;</code>",
                parse_mode="html"
            )

        keyword = parts[1].strip().lower()
        reply = message.reply_to_message

        # Detect content type
        if reply.text:
            content_type = "text"
            content = reply.text
            file_id = None
        elif reply.sticker:
            content_type = "sticker"
            content = None
            file_id = reply.sticker.file_id
        elif reply.photo:
            content_type = "photo"
            content = reply.caption or ""
            file_id = reply.photo.file_id
        elif reply.video:
            content_type = "video"
            content = reply.caption or ""
            file_id = reply.video.file_id
        elif reply.document:
            content_type = "document"
            content = reply.caption or ""
            file_id = reply.document.file_id
        elif reply.audio:
            content_type = "audio"
            content = reply.caption or ""
            file_id = reply.audio.file_id
        elif reply.animation:
            content_type = "animation"
            content = reply.caption or ""
            file_id = reply.animation.file_id
        else:
            return await message.reply_text("⚠️ Unsupported message type for filter.")

        await db.set_filter(message.chat.id, keyword, content_type, content, file_id)
        await message.reply_text(
            f"✅ Filter set for keyword: <code>{keyword}</code>",
            parse_mode="html"
        )


    # ==========================================================
    # /stopfilter <keyword>
    # ==========================================================

    @app.on_message(filters.group & filters.command("stopfilter"))
    async def stopfilter_cmd(client, message: Message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Only admins can use this command.")

        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            return await message.reply_text("⚙️ Usage: <code>/stopfilter &lt;keyword&gt;</code>", parse_mode="html")

        keyword = parts[1].strip().lower()
        removed = await db.delete_filter(message.chat.id, keyword)

        if removed:
            await message.reply_text(f"🗑️ Filter for <code>{keyword}</code> removed.", parse_mode="html")
        else:
            await message.reply_text(f"⚠️ No filter found for <code>{keyword}</code>.", parse_mode="html")


    # ==========================================================
    # /filters — list all
    # ==========================================================

    @app.on_message(filters.group & filters.command("filters"))
    async def filters_list_cmd(client, message: Message):
        all_filters = await db.get_all_filters(message.chat.id)

        if not all_filters:
            return await message.reply_text("📭 No active filters in this group.")

        lines = "\n".join(f"• <code>{k}</code> → <i>{v['type']}</i>" for k, v in all_filters.items())
        await message.reply_text(
            f"📝 <b>Active Filters:</b>\n\n{lines}",
            parse_mode="html"
        )


    # ==========================================================
    # Enforce — trigger filter on keyword match
    # ==========================================================

    @app.on_message(filters.group & filters.text & ~filters.service, group=11)
    async def enforce_filters(client, message: Message):
        if not message.text:
            return

        all_filters = await db.get_all_filters(message.chat.id)
        if not all_filters:
            return

        text_lower = message.text.lower()

        for keyword, data in all_filters.items():
            if keyword in text_lower:
                try:
                    content_type = data.get("type")
                    content = data.get("content")
                    file_id = data.get("file_id")

                    if content_type == "text":
                        await message.reply_text(content)
                    elif content_type == "sticker":
                        await message.reply_sticker(file_id)
                    elif content_type == "photo":
                        await message.reply_photo(file_id, caption=content)
                    elif content_type == "video":
                        await message.reply_video(file_id, caption=content)
                    elif content_type == "document":
                        await message.reply_document(file_id, caption=content)
                    elif content_type == "audio":
                        await message.reply_audio(file_id, caption=content)
                    elif content_type == "animation":
                        await message.reply_animation(file_id, caption=content)
                except Exception as e:
                    logger.error(f"Filter trigger error: {e}")
                break
