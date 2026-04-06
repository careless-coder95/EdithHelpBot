# ============================================================
# Group Manager Bot — Message Cleaner (Auto Delete)
# Author: Mr. Stark
# ============================================================

from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ChatMemberStatus
import asyncio
import logging
import db

logger = logging.getLogger(__name__)


# ==========================================================
# Helpers
# ==========================================================

def parse_time(time_str: str):
    s = time_str.strip().lower()
    try:
        if s.endswith("m"):
            v = int(s[:-1])
            return v * 60
        elif s.endswith("h"):
            v = int(s[:-1])
            return v * 3600
    except ValueError:
        pass
    return None


def fmt_time(seconds: int) -> str:
    if seconds < 3600:
        m = seconds // 60
        return f"{m} minute{'s' if m != 1 else ''}"
    h = seconds // 3600
    return f"{h} hour{'s' if h != 1 else ''}"


async def is_admin(client: Client, chat_id: int, user_id: int) -> bool:
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except Exception:
        return False


async def schedule_delete(message: Message, delay: int):
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Auto-delete failed for msg {message.id}: {e}")


# ==========================================================
# Help Text
# ==========================================================

CLEANER_HELP_TEXT = """
<b>╔══════════════════╗</b>
<b>   🧹 ᴍᴇssᴧɢᴇ ᴄʟᴇᴧɴᴇʀ</b>
<b>╚══════════════════╝</b>

<b>❖ ᴧᴜᴛᴏᴍᴧᴛɪᴄᴧʟʟʏ ᴅᴇʟᴇᴛᴇs ᴧʟʟ ᴍᴇssᴧɢᴇs ғʀᴏᴍ ʀᴇɢᴜʟᴧʀ ᴜsᴇʀs ᴧғᴛᴇʀ ᴧ sᴇᴛ ᴅᴇʟᴧʏ.</b>

<b>🔧 ᴄᴏᴍᴍᴧɴᴅs:</b>

❍ /cleaner on <b>➻ ᴇɴᴧʙʟᴇ ᴧᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ ✅</b>
❍ /cleaner off <b>➻ ᴅɪsᴧʙʟᴇ ᴧᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ ❌</b>
❍ /setcleandelay <time> <b>➻ sᴇᴛ ᴅᴇʟᴇᴛɪᴏɴ ᴅᴇʟᴧʏ</b>  
  <b>➥ ᴇxᴧᴍᴘʟᴇs: 5ᴍ, 1ʜ, 12ʜ, 24ʜ</b>
❍ /cleanstatus <b>➻ sʜᴏᴡ ᴄᴜʀʀᴇɴᴛ sᴇᴛᴛɪɴɢs</b>

<b>⏱️ ᴛɪᴍᴇ ғᴏʀᴍᴧᴛ:</b>
<b>➥ 5ᴍ = 5 ᴍɪɴᴜᴛᴇs</b>  
<b>➥ 1ʜ = 1 ʜᴏᴜʀ</b>  
<b>➥ ʀᴧɴɢᴇ: 1ᴍ ᴛᴏ 24ʜ — ᴅᴇғᴧᴜʟᴛ: 5ᴍ</b>

<b>ℹ️ ɴᴏᴛᴇs:</b>
<b>➥ ᴧᴅᴍɪɴ ᴍᴇssᴧɢᴇs ᴧʀᴇ ɴᴇᴠᴇʀ ᴅᴇʟᴇᴛᴇᴅ.</b>  
<b>➥ ᴧᴘᴘʟɪᴇs ᴛᴏ ᴧʟʟ ᴛᴇxᴛ ᴧɴᴅ ᴍᴇᴅɪᴧ.</b>  
<b>➥ ᴄᴏᴍᴍᴧɴᴅ ᴍᴇssᴧɢᴇs ᴧᴜᴛᴏ-ᴄʟᴇᴧɴ ᴧғᴛᴇʀ 8 sᴇᴄᴏɴᴅs.</b>

<b>👮 ᴏɴʟʏ ᴧᴅᴍɪɴs ᴄᴧɴ ᴄᴏɴғɪɢᴜʀᴇ ᴛʜɪs.</b>
"""


def register_cleaner_handler(app: Client):

    # ==========================================================
    # /cleaner on/off
    # ==========================================================

    @app.on_message(filters.group & filters.command("cleaner"))
    async def cleaner_cmd(client, message: Message):
        if not await is_admin(client, message.chat.id, message.from_user.id):
            try:
                await message.delete()
            except Exception:
                pass
            return

        parts = message.text.split(maxsplit=1)
        if len(parts) < 2 or parts[1].lower() not in ["on", "off"]:
            status = await db.get_cleaner_status(message.chat.id)
            delay = await db.get_cleandelay(message.chat.id)
            current = "✅ Enabled" if status else "❌ Disabled"
            reply = await message.reply_text(
                f"⚙️ Usage: `/cleaner on` or `/cleaner off`\n\n"
                f"📊 Status: {current}\n"
                f"⏱️ Delay: `{fmt_time(delay)}`"
            )
            await asyncio.sleep(8)
            try:
                await reply.delete()
                await message.delete()
            except Exception:
                pass
            return

        status = parts[1].lower() == "on"
        await db.set_cleaner_status(message.chat.id, status)
        delay = await db.get_cleandelay(message.chat.id)

        if status:
            reply = await message.reply_text(
                f"✅ **Message Cleaner ON!**\n\n"
                f"All regular user messages will be deleted after `{fmt_time(delay)}`."
            )
        else:
            reply = await message.reply_text("⚠️ **Message Cleaner OFF!**")

        await asyncio.sleep(8)
        try:
            await reply.delete()
            await message.delete()
        except Exception:
            pass


    # ==========================================================
    # /setcleandelay <time>
    # ==========================================================

    @app.on_message(filters.group & filters.command("setcleandelay"))
    async def setcleandelay_cmd(client, message: Message):
        if not await is_admin(client, message.chat.id, message.from_user.id):
            try:
                await message.delete()
            except Exception:
                pass
            return

        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            # Quick pick buttons
            buttons = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("1 min",  callback_data="cleantime_60"),
                    InlineKeyboardButton("5 min",  callback_data="cleantime_300"),
                    InlineKeyboardButton("15 min", callback_data="cleantime_900"),
                ],
                [
                    InlineKeyboardButton("1 hr",  callback_data="cleantime_3600"),
                    InlineKeyboardButton("6 hr",  callback_data="cleantime_21600"),
                    InlineKeyboardButton("24 hr", callback_data="cleantime_86400"),
                ],
            ])
            reply = await message.reply_text(
                "⏱️ Choose a delay or use `/setcleandelay 5m`:",
                reply_markup=buttons
            )
            await asyncio.sleep(20)
            try:
                await reply.delete()
                await message.delete()
            except Exception:
                pass
            return

        delay = parse_time(parts[1])

        if delay is None:
            reply = await message.reply_text("❌ Invalid format! Use: `5m` `1h` `12h` `24h`")
            await asyncio.sleep(5)
            try:
                await reply.delete()
                await message.delete()
            except Exception:
                pass
            return

        if delay < 60:
            reply = await message.reply_text("❌ Minimum delay is `1m`.")
            await asyncio.sleep(5)
            try:
                await reply.delete()
                await message.delete()
            except Exception:
                pass
            return

        if delay > 86400:
            reply = await message.reply_text("❌ Maximum delay is `24h`.")
            await asyncio.sleep(5)
            try:
                await reply.delete()
                await message.delete()
            except Exception:
                pass
            return

        await db.set_cleandelay(message.chat.id, delay)
        status = await db.get_cleaner_status(message.chat.id)
        status_text = "✅ Cleaner is ON." if status else "⚠️ Cleaner is OFF. Use `/cleaner on` to enable."

        reply = await message.reply_text(
            f"✅ Delay set to `{fmt_time(delay)}`.\n{status_text}"
        )
        await asyncio.sleep(8)
        try:
            await reply.delete()
            await message.delete()
        except Exception:
            pass


    # ==========================================================
    # Quick pick callback — cleantime_<seconds>
    # ==========================================================

    @app.on_callback_query(filters.regex(r"^cleantime_(\d+)$"))
    async def cleantime_callback(client, callback_query):
        delay = int(callback_query.matches[0].group(1))
        chat_id = callback_query.message.chat.id

        if not await is_admin(client, chat_id, callback_query.from_user.id):
            return await callback_query.answer("❌ Only admins can change this.", show_alert=True)

        await db.set_cleandelay(chat_id, delay)
        await callback_query.message.edit_text(
            f"✅ Delay set to **{fmt_time(delay)}**."
        )
        await callback_query.answer()


    # ==========================================================
    # /cleanstatus
    # ==========================================================

    @app.on_message(filters.group & filters.command("cleanstatus"))
    async def cleanstatus_cmd(client, message: Message):
        status = await db.get_cleaner_status(message.chat.id)
        delay = await db.get_cleandelay(message.chat.id)

        reply = await message.reply_text(
            f"📊 **Message Cleaner Status**\n\n"
            f"{'✅ Enabled' if status else '❌ Disabled'}\n"
            f"⏱️ Delay: `{fmt_time(delay)}`"
        )
        await asyncio.sleep(10)
        try:
            await reply.delete()
            await message.delete()
        except Exception:
            pass


    # ==========================================================
    # Enforce — auto delete messages in background
    # ==========================================================

    @app.on_message(filters.group & (filters.text | filters.media) & ~filters.service, group=9)
    async def enforce_cleaner(client, message: Message):
        if not message.from_user or message.from_user.is_bot:
            return

        if not await db.get_cleaner_status(message.chat.id):
            return

        if await is_admin(client, message.chat.id, message.from_user.id):
            return

        delay = await db.get_cleandelay(message.chat.id)
        asyncio.get_event_loop().create_task(
            schedule_delete(message, delay)
        )
