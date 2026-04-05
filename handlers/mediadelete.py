# ============================================================
# Group Manager Bot — Media Auto Delete
# Author: Mr. Stark
# ============================================================

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus
import asyncio
import re
import logging
import db

logger = logging.getLogger(__name__)


async def is_power(client, chat_id: int, user_id: int) -> bool:
    member = await client.get_chat_member(chat_id, user_id)
    return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]


# ==========================================================
# Time Parser — "5m", "1h", "24h" → seconds
# ==========================================================

def parse_time(text: str):
    match = re.fullmatch(r"(\d+)(m|h)", text.strip().lower())
    if not match:
        return None
    value, unit = int(match.group(1)), match.group(2)
    seconds = value * 60 if unit == "m" else value * 3600
    if seconds < 60 or seconds > 86400:
        return None
    return seconds


def seconds_to_readable(s: int) -> str:
    return f"{s // 60}m" if s < 3600 else f"{s // 3600}h"


# ==========================================================
# Background delete task
# ==========================================================

async def delete_after(message: Message, delay: int):
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except Exception:
        pass


# ==========================================================
# Help Text
# ==========================================================
MEDIADELETE_HELP_TEXT = """
<b>╔══════════════════╗</b>
<b>   🎬 ᴍᴇᴅɪᴀ ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ</b>
<b>╚══════════════════╝</b>

<b>❖ Aᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ʀᴇᴍᴏᴠᴇs ᴍᴇᴅɪᴀ ᴍᴇssᴀɢᴇs ᴀғᴛᴇʀ ᴀ ᴄᴏɴғɪɢᴜʀᴇᴅ ᴅᴇʟᴀʏ.</b>

<b>🔧 ᴄᴏᴍᴍᴀɴᴅs:</b>
❍ /mediadelete on <b>➻ ᴇɴᴀʙʟᴇ ᴍᴇᴅɪᴀ ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ ✅</b>
❍ /mediadelete off <b>➻ ᴅɪsᴀʙʟᴇ ᴍᴇᴅɪᴀ ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ ❌</b>
❍ /setmediadelay <time> <b>➻ sᴇᴛ ᴅᴇʟᴀʏ ʙᴇғᴏʀᴇ ᴅᴇʟᴇᴛɪᴏɴ</b>
  
<b>⏱️ ᴛɪᴍᴇ ғᴏʀᴍᴀᴛ:</b>
<b>➥ 5m = 5 ᴍɪɴᴜᴛᴇs</b>  
<b>➥ 1h = 1 ʜᴏᴜʀ</b>  
<b>➥ 12h = 12 ʜᴏᴜʀs</b>  
<b>➥ 24h = 24 ʜᴏᴜʀs</b>  
<b>➥ ʀᴀɴɢᴇ: 1m ᴛᴏ 24h — ᴅᴇғᴀᴜʟᴛ: 5m</b>

<b>ℹ️ ᴀᴘᴘʟɪᴇs ᴛᴏ:</b>
<b>➥ ᴘʜᴏᴛᴏs, ᴠɪᴅᴇᴏs, sᴛɪᴄᴋᴇʀs, ɢɪғs</b>  
<b>➥ ᴀɴɪᴍᴀᴛɪᴏɴs, ʟᴏᴄᴀᴛɪᴏɴs ᴀɴᴅ ᴘᴏʟʟs</b>

<b>👮 Only admins can configure this.</b>
"""


def register_mediadelete_handler(app: Client):

    # ==========================================================
    # /mediadelete on/off
    # ==========================================================

    @app.on_message(filters.group & filters.command("mediadelete"))
    async def mediadelete_cmd(client, message: Message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Only admins can use this command.")

        parts = message.text.split(maxsplit=1)
        if len(parts) < 2 or parts[1].lower() not in ["on", "off"]:
            status = await db.get_mediadelete_status(message.chat.id)
            delay = await db.get_mediadelay(message.chat.id)
            current = "🟢 ON" if status else "🔴 OFF"
            return await message.reply_text(
                f"⚙️ Usage: `/mediadelete on` or `/mediadelete off`\n\n"
                f"📊 Status: {current}\n"
                f"⏱️ Delay: `{seconds_to_readable(delay)}`"
            )

        status = parts[1].lower() == "on"
        await db.set_mediadelete_status(message.chat.id, status)

        if status:
            delay = await db.get_mediadelay(message.chat.id)
            await message.reply_text(
                f"✅ **Media Auto-Delete ON!**\n\n"
                f"Photos, videos, stickers, GIFs, animations,\n"
                f"locations and polls will be deleted after `{seconds_to_readable(delay)}`."
            )
        else:
            await message.reply_text("⚠️ **Media Auto-Delete OFF!**")


    # ==========================================================
    # /setmediadelay <time>
    # ==========================================================

    @app.on_message(filters.group & filters.command("setmediadelay"))
    async def setmediadelay_cmd(client, message: Message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Only admins can use this command.")

        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            delay = await db.get_mediadelay(message.chat.id)
            return await message.reply_text(
                f"⚙️ Usage: `/setmediadelay <time>`\n\n"
                f"Format: `5m` `1h` `12h` `24h`\n"
                f"Range: 1m to 24h\n"
                f"⏱️ Current: `{seconds_to_readable(delay)}`"
            )

        seconds = parse_time(parts[1])
        if not seconds:
            return await message.reply_text(
                "⚠️ Invalid format!\n\n"
                "Use: `5m` `1h` `12h` `24h`\n"
                "Range: 1m to 24h"
            )

        await db.set_mediadelay(message.chat.id, seconds)
        await message.reply_text(f"✅ Media delete delay set to `{seconds_to_readable(seconds)}`.")


    # ==========================================================
    # Enforce — detect media and schedule deletion
    # ==========================================================

    @app.on_message(filters.group & ~filters.service, group=8)
    async def enforce_mediadelete(client, message: Message):
        if not (message.photo or message.video or message.sticker or
                message.animation or message.document or message.location or message.poll):
            return

        if not await db.get_mediadelete_status(message.chat.id):
            return

        delay = await db.get_mediadelay(message.chat.id)
        asyncio.ensure_future(delete_after(message, delay))
