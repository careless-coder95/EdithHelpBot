# ============================================================
# Group Manager Bot — Utility
# Author: Mr. Stark
# ============================================================

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus, ChatType
import logging

logger = logging.getLogger(__name__)


async def is_power(client, chat_id: int, user_id: int) -> bool:
    member = await client.get_chat_member(chat_id, user_id)
    return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]


# ==========================================================
# Help Text
# ==========================================================

UTILITY_HELP_TEXT = """
<b>╔══════════════════╗</b>
<b>   ⚙️ ᴜᴛɪʟɪᴛʏ</b>
<b>╚══════════════════╝</b>

<b>📋 ᴄᴏᴍᴍᴀɴᴅs ❖</b>

❍ /chatinfo <b>➥ ᴠɪᴇᴡ ɢʀᴏᴜᴘ ᴅᴇᴛᴀɪʟs ᴀɴᴅ ᴍᴇᴍʙᴇʀ ᴄᴏᴜɴᴛ</b>
❍ /id <b>➥ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ɪᴅ. ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ</b>  
  <b>➥ ᴛᴏ ɢᴇᴛ ᴛʜᴇɪʀ ɪᴅ.</b>
❍ /pin <b>➥ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ —</b>  
  <b>➥ ɪᴛ ᴡɪʟʟ ʙᴇ ᴘɪɴɴᴇᴅ.</b>
❍ /unpin <b>➥ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ —</b>  
  <b>➥ ɪᴛ ᴡɪʟʟ ʙᴇ ᴜɴᴘɪɴɴᴇᴅ.</b>
❍ /purge <b>➥ ʀᴇᴘʟʏ ғʀᴏᴍ ᴡʜᴇʀᴇ ᴛᴏ sᴛᴀʀᴛ —</b>  
  <b>➥ ᴀʟʟ ᴍᴇssᴀɢᴇs ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ ᴜɴᴛɪʟ ɴᴏᴡ.</b>
❍ /del <b>➥ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ —</b>  
  <b>➥ ᴏɴʟʏ ᴛʜᴀᴛ ᴍᴇssᴀɢᴇ ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ.</b>
❍ /report <b>➥ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ —</b>  
  <b>➥ ᴀᴅᴍɪɴs ᴡɪʟʟ ʙᴇ ɴᴏᴛɪғɪᴇᴅ.</b>

<b>👮 /pin, /purge, /del — ᴀᴅᴍɪɴ ᴏɴʟʏ.</b>  
<b>👥 /report — ᴀᴠᴀɪʟᴀʙʟᴇ ғᴏʀ ᴀʟʟ ᴜsᴇʀs.</b>
"""


def register_utility_handler(app: Client):

    # ==========================================================
    # /chatinfo
    # ==========================================================

    @app.on_message(filters.group & filters.command("chatinfo"))
    async def chatinfo_cmd(client, message: Message):
        chat = message.chat
        try:
            count = await client.get_chat_members_count(chat.id)
        except:
            count = "N/A"

        username = f"@{chat.username}" if chat.username else "Private Group"
        chat_type = str(chat.type).replace("ChatType.", "").capitalize()

        text = (
            f"╔══════════════════╗\n"
            f"   ℹ️ Chat Info\n"
            f"╚══════════════════╝\n\n"
            f"📛 **Name:** {chat.title}\n"
            f"🆔 **ID:** `{chat.id}`\n"
            f"🔗 **Username:** {username}\n"
            f"👥 **Members:** {count}\n"
            f"📂 **Type:** {chat_type}\n"
        )
        await message.reply_text(text)


    # ==========================================================
    # /id
    # ==========================================================

    @app.on_message(filters.command("id"))
    async def id_cmd(client, message: Message):
        if message.reply_to_message:
            user = message.reply_to_message.from_user
            if user:
                await message.reply_text(
                    f"👤 **{user.first_name}**\n"
                    f"🆔 User ID: `{user.id}`"
                )
            else:
                await message.reply_text("⚠️ User not detected.")
        else:
            user = message.from_user
            text = f"🆔 **Aapka ID:** `{user.id}`"
            if message.chat.type != ChatType.PRIVATE:
                text += f"\n💬 **Chat ID:** `{message.chat.id}`"
            await message.reply_text(text)


    # ==========================================================
    # /pin
    # ==========================================================

    @app.on_message(filters.group & filters.command("pin"))
    async def pin_cmd(client, message: Message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Only admin can pin.")

        if not message.reply_to_message:
            return await message.reply_text("⚠️ Reply to the message you want to pin.")

        try:
            await client.pin_chat_message(
                message.chat.id,
                message.reply_to_message.id,
                disable_notification=False
            )
            await message.reply_text("📌 Message pinned!")
        except Exception as e:
            await message.reply_text(f"❌ Not pinned: {e}")


    # ==========================================================
    # /unpin
    # ==========================================================

    @app.on_message(filters.group & filters.command("unpin"))
    async def unpin_cmd(client, message: Message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Only admin can unpin.")

        try:
            if message.reply_to_message:
                await client.unpin_chat_message(
                    message.chat.id,
                    message.reply_to_message.id
                )
                await message.reply_text("📌 This message got unpinned!")
            else:
                await client.unpin_all_chat_messages(message.chat.id)
                await message.reply_text("📌 All pinned messages have been unpinned!")
        except Exception as e:
            await message.reply_text(f"❌ not unpinned: {e}")
            
    # ==========================================================
    # /purge
    # ==========================================================

    @app.on_message(filters.group & filters.command("purge"))
    async def purge_cmd(client, message: Message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Only the admin can purge.")

        if not message.reply_to_message:
            return await message.reply_text("⚠️ Reply to the message you want to start deleting from..")

        from_msg_id = message.reply_to_message.id
        to_msg_id = message.id

        msg_ids = list(range(from_msg_id, to_msg_id + 1))

        # 100 ke batch mein delete karo (Telegram limit)
        deleted = 0
        for i in range(0, len(msg_ids), 100):
            batch = msg_ids[i:i + 100]
            try:
                await client.delete_messages(message.chat.id, batch)
                deleted += len(batch)
            except Exception as e:
                logger.error(f"Purge batch error: {e}")

        confirm = await client.send_message(
            message.chat.id,
            f"🗑️ **{deleted}** messages got deleted."
        )
        import asyncio
        await asyncio.sleep(3)
        await confirm.delete()


    # ==========================================================
    # /del
    # ==========================================================

    @app.on_message(filters.group & filters.command("del"))
    async def del_cmd(client, message: Message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Only admin can delete it.")

        if not message.reply_to_message:
            return await message.reply_text("⚠️ Reply to the message you want to delete..")

        try:
            await message.reply_to_message.delete()
            await message.delete()
        except Exception as e:
            await message.reply_text(f"❌ not deleted: {e}")


    # ==========================================================
    # /report
    # ==========================================================

    @app.on_message(filters.group & filters.command("report"))
    async def report_cmd(client, message: Message):
        if not message.reply_to_message:
            return await message.reply_text("⚠️ Reply to the message you want to report..")

        reported_user = message.reply_to_message.from_user
        reporter = message.from_user

        if not reported_user:
            return await message.reply_text("⚠️ User not detected.")

        if reported_user.id == reporter.id:
            return await message.reply_text("⚠️ You cannot report yourself.")

        # Sabke admins ko fetch karo
        try:
            admins = []
            async for member in client.get_chat_members(
                message.chat.id,
                filter=ChatMemberStatus.ADMINISTRATOR
            ):
                if not member.user.is_bot:
                    admins.append(member.user.mention)
        except:
            admins = []

        admin_mentions = " ".join(admins) if admins else "Admins"

        await message.reply_text(
            f"🚨 **Report Filed!**\n\n"
            f"👤 **Reported:** {reported_user.mention}\n"
            f"📝 **By:** {reporter.mention}\n"
            f"💬 **Message:** [Click here](https://t.me/c/{str(message.chat.id)[4:]}/{message.reply_to_message.id})\n\n"
            f"📢 {admin_mentions} — please check karo!"
        )
