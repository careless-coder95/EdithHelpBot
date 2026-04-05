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
╔══════════════════╗
   ⚙️ UTILITY
╚══════════════════╝

📋 Commands:

• /chatinfo
  → Group ki details aur member count

• /id
  → Apna ID dekho. Reply karo
    kisi par to uska ID milega.

• /pin
  → Reply karo kisi message par —
    wo message pin ho jaayega.

• /purge
  → Reply karo jis message se delete
    shuru karna hai — sab delete honge
    wahan se ab tak.

• /del
  → Reply karo kisi message par —
    sirf wo message delete hoga.

• /report
  → Reply karo kisi message par —
    admins ko report jaayegi.

👮 pin, purge, del — sirf admin.
👥 report — sab use kar sakte hain.
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
                await message.reply_text("⚠️ User detect nahi hua.")
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
            return await message.reply_text("❌ Sirf admin pin kar sakta hai.")

        if not message.reply_to_message:
            return await message.reply_text("⚠️ Jis message ko pin karna hai usse reply karo.")

        try:
            await client.pin_chat_message(
                message.chat.id,
                message.reply_to_message.id,
                disable_notification=False
            )
            await message.reply_text("📌 Message pin ho gaya!")
        except Exception as e:
            await message.reply_text(f"❌ Pin nahi hua: {e}")


    # ==========================================================
    # /purge
    # ==========================================================

    @app.on_message(filters.group & filters.command("purge"))
    async def purge_cmd(client, message: Message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Sirf admin purge kar sakta hai.")

        if not message.reply_to_message:
            return await message.reply_text("⚠️ Jis message se delete shuru karna hai usse reply karo.")

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
            f"🗑️ **{deleted}** messages delete ho gaye."
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
            return await message.reply_text("❌ Sirf admin delete kar sakta hai.")

        if not message.reply_to_message:
            return await message.reply_text("⚠️ Jis message ko delete karna hai usse reply karo.")

        try:
            await message.reply_to_message.delete()
            await message.delete()
        except Exception as e:
            await message.reply_text(f"❌ Delete nahi hua: {e}")


    # ==========================================================
    # /report
    # ==========================================================

    @app.on_message(filters.group & filters.command("report"))
    async def report_cmd(client, message: Message):
        if not message.reply_to_message:
            return await message.reply_text("⚠️ Jis message ko report karna hai usse reply karo.")

        reported_user = message.reply_to_message.from_user
        reporter = message.from_user

        if not reported_user:
            return await message.reply_text("⚠️ User detect nahi hua.")

        if reported_user.id == reporter.id:
            return await message.reply_text("⚠️ Aap khud ko report nahi kar sakte.")

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
