# ============================================================
# Group Manager Bot — Ghost Mode & Privacy
# Author: Mr. Stark
# ============================================================

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatMemberStatus
import db
import logging

logger = logging.getLogger(__name__)


async def is_power(client, chat_id: int, user_id: int) -> bool:
    member = await client.get_chat_member(chat_id, user_id)
    return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]


GHOST_HELP_TEXT = (
    f"<blockquote expandable>"
    f"<b>╔══════════════════╗</b>\n"
    f"<b>👻 ɢʜᴏsᴛ ᴍᴏᴅᴇ</b>\n"
    f"<b>╚══════════════════╝</b>\n\n"
    
    f"<b>❖ ᴄᴏᴍᴍᴧɴᴅs ❖</b>\n\n"
    f"<b>➻ /ghostmode on — ᴇɴᴧʙʟᴇ ɢʜᴏsᴛ ᴍᴏᴅᴇ ✅</b>\n"
    f"<b>➻ /ghostmode off — ᴅɪsᴧʙʟᴇ ɢʜᴏsᴛ ᴍᴏᴅᴇ ❌</b>\n\n"
    
    f"<b>❖ ᴡʜᴧᴛ ɢᴇᴛs ᴅᴇʟᴇᴛᴇᴅ ❖</b>\n"
    f"<b>➻ ᴜsᴇʀ ᴊᴏɪɴᴇᴅ ᴛʜᴇ ɢʀᴏᴜᴘ</b>\n"
    f"<b>➻ ᴜsᴇʀ ʟᴇғᴛ ᴛʜᴇ ɢʀᴏᴜᴘ</b>\n"
    f"<b>➻ ᴜsᴇʀ ᴡᴧs ʀᴇᴍᴏᴠᴇᴅ</b>\n"
    f"<b>➻ ɢʀᴏᴜᴘ ᴛɪᴛʟᴇ ᴄʜᴧɴɢᴇᴅ</b>\n"
    f"<b>➻ ɢʀᴏᴜᴘ ᴘʜᴏᴛᴏ ᴄʜᴧɴɢᴇᴅ</b>\n"
    f"<b>➻ ᴘɪɴɴᴇᴅ ᴍᴇssᴧɢᴇ ɴᴏᴛɪғɪᴄᴧᴛɪᴏɴs</b>\n"
    f"<b>➻ ᴠɪᴅᴇᴏ ᴄʜᴧᴛ sᴛᴧʀᴛᴇᴅ / ᴇɴᴅᴇᴅ</b>\n\n"
    
    f"<b>👮 𝑂𝑛𝑙𝑦 𝑎𝑑𝑚𝑖𝑛𝑠 𝑐𝑎𝑛 𝑐𝑜𝑛𝑓𝑖𝑔𝑢𝑟𝑒 𝑡ℎ𝑖𝑠.</b>"
    f"</blockquote>"
)


def register_ghost_handler(app: Client):

    # ==========================================================
    # /ghostmode on/off
    # ==========================================================

    @app.on_message(filters.group & filters.command("ghostmode"))
    async def ghostmode_cmd(client, message: Message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text(
                "❌ Only admins can use this command.",
                parse_mode=enums.ParseMode.HTML
            )

        parts = message.text.split(maxsplit=1)
        if len(parts) < 2 or parts[1].lower() not in ["on", "off"]:
            status = await db.get_ghost_status(message.chat.id)
            current = "🟢 ON" if status else "🔴 OFF"
            return await message.reply_text(
                f"⚙️ Usage: <code>/ghostmode on</code> or <code>/ghostmode off</code>\n\n"
                f"📊 Current: {current}",
                parse_mode=enums.ParseMode.HTML
            )

        status = parts[1].lower() == "on"
        await db.set_ghost_status(message.chat.id, status)

        if status:
            await message.reply_text(
                "👻 <b>Ghost Mode ON!</b>\n\n"
                "All service messages will be deleted automatically.",
                parse_mode=enums.ParseMode.HTML
            )
        else:
            await message.reply_text(
                "⚠️ <b>Ghost Mode OFF!</b>",
                parse_mode=enums.ParseMode.HTML
            )


    # ==========================================================
    # Enforce — delete service messages
    # ==========================================================

    @app.on_message(filters.group & filters.service, group=12)
    async def enforce_ghost(client, message: Message):
        if not await db.get_ghost_status(message.chat.id):
            return
        try:
            await message.delete()
        except Exception as e:
            logger.error(f"Ghost mode delete error: {e}")


    # ==========================================================
    # /privacy
    # ==========================================================

    @app.on_message(filters.command("privacy"))
    async def privacy_cmd(client, message: Message):
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton(
                "📄 View Privacy Policy",
                url="https://graph.org/Anya-Bots---Privacy-Policy-04-12"
            )]
        ])
        await message.reply_text(
            "╔══════════════════╗\n"
            "   🔒 PRIVACY POLICY\n"
            "╚══════════════════╝\n\n"
            "This bot collects minimal data required\n"
            "to function properly in your group.\n\n"
            "Click the button below to read our\n"
            "full Privacy Policy.",
            reply_markup=buttons,
            parse_mode=enums.ParseMode.HTML
        )
