# ============================================================
# Group Manager Bot — Force Subscribe
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


async def user_joined_channel(client, user_id: int, channel: str) -> bool:
    """Check karo user channel ka member hai ya nahi"""
    try:
        member = await client.get_chat_member(channel, user_id)
        return member.status not in [ChatMemberStatus.BANNED, ChatMemberStatus.LEFT]
    except Exception as e:
        logger.error(f"FSub check error ({channel}): {e}")
        return False  # Error pe rokna nahi


def register_fsub_handler(app: Client):

    # ==========================================================
    # /addfsub <channel> — Channel add karo
    # ==========================================================

    @app.on_message(filters.group & filters.command("addfsub"))
    async def addfsub_cmd(client, message: Message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Sirf admin hi yeh command use kar sakta hai.")

        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            return await message.reply_text(
                "⚙️ Usage: `/addfsub @channelname` ya `/addfsub -100xxxxxxxxxx`"
            )

        channel = parts[1].strip()

        # Verify karo ki channel exist karta hai aur bot admin hai
        try:
            chat = await client.get_chat(channel)
            channel_id = str(chat.id)
        except Exception as e:
            return await message.reply_text(f"❌ Channel nahi mila: `{channel}`\nBot ko channel ka admin banana padega.")

        existing = await db.get_fsub_channels(message.chat.id)
        if channel_id in existing:
            return await message.reply_text(f"⚠️ `{chat.title}` pehle se add hai.")

        await db.add_fsub_channel(message.chat.id, channel_id)
        await message.reply_text(
            f"✅ **{chat.title}** force-subscribe list mein add ho gaya!\n\n"
            f"Ab jo user is channel mein nahi hoga, uska message delete hoga."
        )

    # ==========================================================
    # /removefsub <channel> — Channel remove karo
    # ==========================================================

    @app.on_message(filters.group & filters.command("removefsub"))
    async def removefsub_cmd(client, message: Message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Sirf admin hi yeh command use kar sakta hai.")

        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            return await message.reply_text("⚙️ Usage: `/removefsub @channelname`")

        channel = parts[1].strip()
        try:
            chat = await client.get_chat(channel)
            channel_id = str(chat.id)
            title = chat.title
        except:
            channel_id = channel
            title = channel

        removed = await db.remove_fsub_channel(message.chat.id, channel_id)
        if removed:
            await message.reply_text(f"🗑️ `{title}` force-subscribe list se hata diya gaya.")
        else:
            await message.reply_text(f"⚠️ `{title}` list mein tha hi nahi.")

    # ==========================================================
    # /fsublist — Sab channels dikhao
    # ==========================================================

    @app.on_message(filters.group & filters.command("fsublist"))
    async def fsublist_cmd(client, message: Message):
        channels = await db.get_fsub_channels(message.chat.id)

        if not channels:
            return await message.reply_text("📭 Koi force-subscribe channel add nahi hai.\n`/addfsub @channel` se add karo.")

        text = "╔══════════════════╗\n   🔗 Force-Subscribe List\n╚══════════════════╝\n\n"
        for i, ch_id in enumerate(channels, 1):
            try:
                chat = await client.get_chat(int(ch_id))
                username = f"@{chat.username}" if chat.username else f"`{ch_id}`"
                text += f"{i}. {chat.title} — {username}\n"
            except:
                text += f"{i}. `{ch_id}`\n"

        await message.reply_text(text)

    # ==========================================================
    # Enforce FSub — har message check karo
    # ==========================================================

    @app.on_message(filters.group & ~filters.service, group=3)
    async def enforce_fsub(client, message: Message):
        try:
            member = await client.get_chat_member(message.chat.id, message.from_user.id)
            if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                return
        except:
            return

        channels = await db.get_fsub_channels(message.chat.id)
        if not channels:
            return

        not_joined = []
        for ch_id in channels:
            joined = await user_joined_channel(client, message.from_user.id, int(ch_id))
            if not joined:
                try:
                    chat = await client.get_chat(int(ch_id))
                    if chat.username:
                        not_joined.append((chat.title, f"https://t.me/{chat.username}"))
                    else:
                        not_joined.append((chat.title, None))
                except:
                    not_joined.append((f"`{ch_id}`", None))

        if not not_joined:
            return

        try:
            await message.delete()
        except:
            pass

        # Join buttons banao
        buttons = []
        for title, link in not_joined:
            if link:
                buttons.append([InlineKeyboardButton(f"📢 Join {title}", url=link)])

        text = (
            f"⛔ {message.from_user.mention}, pehle neeche diye channels join karo!\n\n"
            f"Join karne ke baad dobara message karo. ✅"
        )

        try:
            if buttons:
                warn = await client.send_message(
                    message.chat.id, text,
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
            else:
                warn = await client.send_message(message.chat.id, text)

            import asyncio
            await asyncio.sleep(30)
            await warn.delete()
        except Exception as e:
            logger.error(f"FSub warn error: {e}")
