# ============================================================
# Group Manager Bot — Tools
# Author: Mr. Stark
# ============================================================

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus
import db
import re
import aiohttp
import logging

logger = logging.getLogger(__name__)


async def is_power(client, chat_id: int, user_id: int) -> bool:
    member = await client.get_chat_member(chat_id, user_id)
    return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]


# ==========================================================
# Patterns
# ==========================================================

PHONE_PATTERN = re.compile(
    r"(\+?\d[\d\s\-]{7,14}\d)",
    re.IGNORECASE
)

HASHTAG_PATTERN = re.compile(r"#\w+")


# ==========================================================
# Telegraph upload helper
# ==========================================================

async def upload_to_telegraph(title: str, content: str) -> str | None:
    """Text ko Telegraph par upload karo aur link return karo"""
    try:
        async with aiohttp.ClientSession() as session:
            # Account create
            async with session.post("https://api.telegra.ph/createAccount", json={
                "short_name": "NomadeBot",
                "author_name": "Nomade Help Bot"
            }) as resp:
                data = await resp.json()
                token = data["result"]["access_token"]

            # Page create
            async with session.post("https://api.telegra.ph/createPage", json={
                "access_token": token,
                "title": title or "Message",
                "content": [{"tag": "p", "children": [content]}],
                "return_content": False
            }) as resp:
                data = await resp.json()
                return data["result"]["url"]
    except Exception as e:
        logger.error(f"Telegraph upload error: {e}")
        return None


# ==========================================================
# Help Texts
# ==========================================================
LONGMSG_HELP_TEXT = """
<b>╔══════════════════╗</b>
<b>   📄 ʟᴏɴɢ ᴍᴇssᴀɢᴇ</b>
<b>╚══════════════════╝</b>

<b>❖ ʟᴏɴɢ ᴍᴇssᴀɢᴇs ᴜᴘʟᴏᴀᴅ ᴛᴏ ᴛᴇʟᴇɢʀᴀᴘʜ ᴀɴᴅ sᴇɴᴅ ᴀs ʟɪɴᴋs.</b>

❍ /echo <text> <b>➻ ʀᴇᴘʟʏ ᴡɪᴛʜ ᴛʜᴇ sᴀᴍᴇ ᴛᴇxᴛ. ɪғ ʟᴏɴɢ, ɢᴇᴛ ᴀ ᴛᴇʟᴇɢʀᴀᴘʜ ʟɪɴᴋ.</b>
❍ /setlongmode off <b>➻ ɴᴏ ᴀᴄᴛɪᴏɴ ᴏɴ ʟᴏɴɢ ᴍᴇssᴀɢᴇs.</b>
❍ /setlongmode manual <b>➻ ᴅᴇʟᴇᴛᴇ + ᴡᴀʀɴ ᴜsᴇʀ.</b>
❍ /setlongmode automatic ✅ ᴅᴇғᴀᴜʟᴛ <b>➻ ᴅᴇʟᴇᴛᴇ + ᴛᴇʟᴇɢʀᴀᴘʜ ʟɪɴᴋ ᴄʀᴇᴀᴛᴇ.</b>
❍ /setlonglimit <50–2000> <b>➻ sᴇᴛ ᴄʜᴀʀᴀᴄᴛᴇʀ ʟɪᴍɪᴛ. ᴅᴇғᴀᴜʟᴛ: 800.</b>
<b>👮 ᴍᴏᴅᴇ/ʟɪᴍɪᴛ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ sᴇᴛ.</b>
"""


PHONE_HELP_TEXT = """
<b>╔══════════════════╗</b>
<b>   📞 ᴘʜᴏɴᴇ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ</b>
<b>╚══════════════════╝</b>

<b>❖ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ ᴍᴇssᴀɢᴇs ᴀʀᴇ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴅᴇʟᴇᴛᴇᴅ.</b>
❍ /nophone on  ➻ <b>ʙʟᴏᴄᴋ ✅</b>  
❍ /nophone off ➻ <b>ᴀʟʟᴏᴡ ❌</b>

<b>❖ ᴅᴇᴛᴇᴄᴛɪᴏɴ ᴇxᴀᴍᴘʟᴇs:</b>
➻ +91 9876543210  
➻ +1-234-567-8900  
➻ 919876543210

<b>ℹ️ Phone messages will be deleted automatically.</b>  
<b>👮 Only admins can configure this.</b>
"""

HASHTAG_HELP_TEXT = """
<b>╔══════════════════╗</b>
<b>   # ʜᴀsʜᴛᴀɢ ꜰɪʟᴛᴇʀ</b>
<b>╚══════════════════╝</b>

<b>❖ Hashtag messages ᴀʀᴇ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴅᴇʟᴇᴛᴇᴅ.</b>
❍ /nohashtags on  ➻ <b>ʙʟᴏᴄᴋ ✅</b>  
❍ /nohashtags off ➻ <b>ᴀʟʟᴏᴡ ❌</b>

<b>❖ ᴅᴇᴛᴇᴄᴛɪᴏɴ ᴇxᴀᴍᴘʟᴇs:</b>
➻ #join, #promotion, #trending  
➻ Any word starting with #

<b>ℹ️ Hashtag messages will be deleted automatically.</b>  
<b>👮 Only admins can configure this.</b>
"""


def register_tools_handler(app: Client):

    # ==========================================================
    # /echo
    # ==========================================================

    @app.on_message(filters.group & filters.command("echo"))
    async def echo_cmd(client, message: Message):
        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            return await message.reply_text("⚙️ Usage: `/echo <text>`")

        text = parts[1]
        limit = await db.get_longlimit(message.chat.id)

        if len(text) <= limit:
            await message.reply_text(text)
        else:
            link = await upload_to_telegraph("Echo", text)
            if link:
                await message.reply_text(f"📄 The message was very long – uploaded to the Telegraph:\n{link}")
            else:
                await message.reply_text("❌ Telegraph upload failed. Try later.")


    # ==========================================================
    # /setlongmode
    # ==========================================================

    @app.on_message(filters.group & filters.command("setlongmode"))
    async def setlongmode_cmd(client, message: Message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Only admin can use this command.")

        parts = message.text.split(maxsplit=1)
        if len(parts) < 2 or parts[1].lower() not in ["off", "manual", "automatic"]:
            mode = await db.get_longmode(message.chat.id)
            return await message.reply_text(
                f"⚙️ Usage: `/setlongmode off|manual|automatic`\n\n📊 Current: `{mode}`"
            )

        mode = parts[1].lower()
        await db.set_longmode(message.chat.id, mode)

        info = {
            "off": "⚠️ There will be no action on long messages.",
            "manual": "🗑️ Long message will be deleted + user will be warned.",
            "automatic": "📄 Long message will be deleted + Telegraph link will be sent.",
        }
        await message.reply_text(f"✅ Long message mode: `{mode}`\n\n{info[mode]}")


    # ==========================================================
    # /setlonglimit
    # ==========================================================

    @app.on_message(filters.group & filters.command("setlonglimit"))
    async def setlonglimit_cmd(client, message: Message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Only admin can use this command.")

        parts = message.text.split(maxsplit=1)
        if len(parts) < 2 or not parts[1].strip().isdigit():
            limit = await db.get_longlimit(message.chat.id)
            return await message.reply_text(
                f"⚙️ Usage: `/setlonglimit <200–4000>`\n\n📊 Current limit: `{limit}` characters"
            )

        num = int(parts[1].strip())
        if not (50 <= num <= 4000):
            return await message.reply_text("⚠️ The limit should be between 50 to 2000")

        await db.set_longlimit(message.chat.id, num)
        await message.reply_text(f"✅ Long message limit set: `{num}` characters")


    # ==========================================================
    # Enforce long message — group messages check karo
    # ==========================================================

    @app.on_message(filters.group & filters.text & ~filters.service, group=4)
    async def enforce_longmsg(client, message: Message):
        try:
            member = await client.get_chat_member(message.chat.id, message.from_user.id)
            if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                return
        except:
            return

        mode = await db.get_longmode(message.chat.id)
        if mode == "off":
            return

        limit = await db.get_longlimit(message.chat.id)
        if not message.text or len(message.text) <= limit:
            return

        await message.delete()

        if mode == "manual":
            await client.send_message(
                message.chat.id,
                f"⚠️ {message.from_user.mention}, Your message was very long ({len(message.text)} chars).\n"
                f"Please send messages smaller than {limit} characters."
            )
        elif mode == "automatic":
            link = await upload_to_telegraph(
                f"Message by {message.from_user.first_name}",
                message.text
            )
            if link:
                await client.send_message(
                    message.chat.id,
                    f"📄 {message.from_user.mention}'s length message got uploaded on Telegraph:\n{link}"
                )


    # ==========================================================
    # /nophone
    # ==========================================================

    @app.on_message(filters.group & filters.command("nophone"))
    async def nophone_cmd(client, message: Message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Only Admin can use this command.")

        parts = message.text.split(maxsplit=1)
        if len(parts) < 2 or parts[1].lower() not in ["on", "off"]:
            status = await db.get_nophone_status(message.chat.id)
            current = "🟢 ON" if status else "🔴 OFF"
            return await message.reply_text(
                f"⚙️ Usage: `/nophone on` ya `/nophone off`\n\n📊 Current: {current}"
            )

        status = parts[1].lower() == "on"
        await db.set_nophone_status(message.chat.id, status)
        await message.reply_text(
            "✅ **Phone Protection ON!**\n\nPhone number like messages will be deleted. 📵"
            if status else
            "⚠️ **Phone Protection OFF!**"
        )


    # ==========================================================
    # Enforce phone
    # ==========================================================

    @app.on_message(filters.group & filters.text & ~filters.service, group=5)
    async def enforce_nophone(client, message: Message):
        try:
            member = await client.get_chat_member(message.chat.id, message.from_user.id)
            if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                return
        except:
            return

        if not await db.get_nophone_status(message.chat.id):
            return

        if message.text and PHONE_PATTERN.search(message.text):
            await message.delete()


    # ==========================================================
    # /nohashtags
    # ==========================================================

    @app.on_message(filters.group & filters.command("nohashtags"))
    async def nohashtags_cmd(client, message: Message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Only Admins can use thos command bebe.")

        parts = message.text.split(maxsplit=1)
        if len(parts) < 2 or parts[1].lower() not in ["on", "off"]:
            status = await db.get_nohashtag_status(message.chat.id)
            current = "🟢 ON" if status else "🔴 OFF"
            return await message.reply_text(
                f"⚙️ Usage: `/nohashtags on` ya `/nohashtags off`\n\n📊 Current: {current}"
            )

        status = parts[1].lower() == "on"
        await db.set_nohashtag_status(message.chat.id, status)
        await message.reply_text(
            "✅ **Hashtag Filter ON!**\n\nNow Messages with hashtags will be deleted. 🚫#"
            if status else
            "⚠️ **Hashtag Filter OFF!**"
        )


    # ==========================================================
    # Enforce hashtag
    # ==========================================================

    @app.on_message(filters.group & filters.text & ~filters.service, group=6)
    async def enforce_nohashtag(client, message: Message):
        try:
            member = await client.get_chat_member(message.chat.id, message.from_user.id)
            if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                return
        except:
            return

        if not await db.get_nohashtag_status(message.chat.id):
            return

        if message.text and HASHTAG_PATTERN.search(message.text):
            await message.delete()
