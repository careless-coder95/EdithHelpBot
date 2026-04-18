# ============================================================
# Group Manager Bot — Auto Accept Join Requests
# Author: Mr. Stark
# ============================================================

from pyrogram import Client, filters
from pyrogram.types import (
    Message, ChatJoinRequest,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from pyrogram.enums import ChatMemberStatus
from pyrogram import Client, filters, enums
import db
import logging

logger = logging.getLogger(__name__)


async def is_power(client, chat_id: int, user_id: int) -> bool:
    member = await client.get_chat_member(chat_id, user_id)
    return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]


JOINREQUEST_HELP_TEXT = (
    f"<blockquote expandable>"
    f"<b>╔════════════════════════╗</b>\n"
    f"<b>🤖 ᴧᴜᴛᴏ ᴧᴄᴄᴇᴘᴛ – ᴊᴏɪɴ ʀᴇǫᴜᴇsᴛs</b>\n"
    f"<b>╚════════════════════════╝</b>\n\n"
    
    f"<b>❖ ᴄᴏᴍᴍᴧɴᴅs ❖</b>\n\n"
    f"<b>➻ /acceptall on — ᴧᴜᴛᴏ ᴧᴄᴄᴇᴘᴛ ᴏɴ ✅</b>\n"
    f"<b>➻ /acceptall off — ᴧᴜᴛᴏ ᴧᴄᴄᴇᴘᴛ ᴏғғ ❌</b>\n\n"
    
    f"<b>❖ ᴡʜᴇɴ ᴏғғ ❖</b>\n"
    f"<b>➻ ʙᴏᴛ sᴇɴᴅs ᴧ ᴊᴏɪɴ ʀᴇǫᴜᴇsᴛ ɴᴏᴛɪғɪᴄᴧᴛɪᴏɴ</b>\n"
    f"<b>➻ ᴛᴏ ᴛʜᴇ ɢʀᴏᴜᴘ ᴡɪᴛʜ ᴧᴘᴘʀᴏᴠᴇ / ᴅᴇᴄʟɪɴᴇ</b>\n"
    f"<b>➻ ʙᴜᴛᴛᴏɴs ғᴏʀ ᴧᴅᴍɪɴs</b>\n\n"
    
    f"<b>❖ ɴᴏᴛᴇs ❖</b>\n"
    f"<b>➻ ʙᴏᴛ ᴍᴜsᴛ ʙᴇ ᴧᴅᴍɪɴ ᴡɪᴛʜ ᴧᴘᴘʀᴏᴠᴧʟ ʀɪɢʜᴛs</b>\n"
    f"<b>➻ ᴡᴏʀᴋs ᴏɴʟʏ ᴡɪᴛʜ ᴊᴏɪɴ ʀᴇǫᴜᴇsᴛ ʟɪɴᴋs</b>\n"
    f"<b>➻ ᴏɴʟʏ ᴧᴅᴍɪɴs ᴄᴧɴ ᴧᴘᴘʀᴏᴠᴇ ᴏʀ ᴅᴇᴄʟɪɴᴇ</b>"
    f"</blockquote>"
)

def register_joinrequest_handler(app: Client):

    # ==========================================================
    # /acceptall on/off
    # ==========================================================

    @app.on_message(filters.group & filters.command("acceptall"))
    async def acceptall_cmd(client, message: Message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Only admins can use this command.")

        parts = message.text.split(maxsplit=1)
        if len(parts) < 2 or parts[1].lower() not in ["on", "off"]:
            status = await db.get_acceptall_status(message.chat.id)
            current = "🟢 ON" if status else "🔴 OFF"
            return await message.reply_text(
                f"⚙️ Usage: <code>/acceptall on</code> or <code>/acceptall off</code>\n\n"
                f"📊 Current: {current}",
                parse_mode=enums.ParseMode.HTML
            )

        status = parts[1].lower() == "on"
        await db.set_acceptall_status(message.chat.id, status)

        if status:
            await message.reply_text(
                "✅ <b>Auto Accept ON!</b>\n\n"
                "All join requests will be approved automatically.",
                parse_mode=enums.ParseMode.HTML
            )
        else:
            await message.reply_text(
                "⚠️ <b>Auto Accept OFF!</b>\n\n"
                "Admins will be notified for each join request.",
                parse_mode=enums.ParseMode.HTML
            )


    # ==========================================================
    # Handle join request event
    # ==========================================================

    @app.on_chat_join_request()
    async def handle_join_request(client, request: ChatJoinRequest):
        chat_id = request.chat.id
        user = request.from_user

        auto_accept = await db.get_acceptall_status(chat_id)

        if auto_accept:
            # Auto approve
            try:
                await client.approve_chat_join_request(chat_id, user.id)
                logger.info(f"Auto approved {user.id} in {chat_id}")
            except Exception as e:
                logger.error(f"Auto approve error: {e}")
            return

        # Manual mode — notify admins with buttons
        username = f"@{user.username}" if user.username else "N/A"
        name = user.first_name + (f" {user.last_name}" if user.last_name else "")

        text = (
            f"𝑁𝑒𝑤 𝑗𝑜𝑖𝑛 𝑅𝑒𝑞𝑢𝑒𝑠𝑡\n"
            f"❍ 𝑈𝑠𝑒𝑟 𝑖𝑛𝑓𝑜\n\n"
            f":⧽ 𝑛𝑎𝑚𝑒: <b>{name}</b>\n"
            f":⧽ 𝑢𝑠𝑒𝑟: <code>{username}</code>\n"
            f":⧽ 𝑖𝑑: <code>{user.id}</code>"
        )

        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Approve", callback_data=f"jr_approve_{chat_id}_{user.id}"),
                InlineKeyboardButton("❌ Decline", callback_data=f"jr_decline_{chat_id}_{user.id}"),
            ]
        ])

        try:
            await client.send_message(
                chat_id,
                text,
                reply_markup=buttons,
                parse_mode=enums.ParseMode.HTML
            )
        except Exception as e:
            logger.error(f"Join request notify error: {e}")


    # ==========================================================
    # Approve callback
    # ==========================================================

    @app.on_callback_query(filters.regex(r"^jr_approve_(-?\d+)_(\d+)$"))
    async def jr_approve_callback(client, callback_query):
        chat_id = int(callback_query.matches[0].group(1))
        user_id = int(callback_query.matches[0].group(2))

        # Only admins can approve
        if not await is_power(client, chat_id, callback_query.from_user.id):
            return await callback_query.answer("❌ Only admins can approve.", show_alert=True)

        try:
            await client.approve_chat_join_request(chat_id, user_id)
            user = await client.get_users(user_id)
            await callback_query.message.edit_text(
                f"✅ <b>Approved!</b>\n\n"
                f":⧽ 𝑛𝑎𝑚𝑒: <b>{user.first_name}</b>\n"
                f":⧽ 𝑖𝑑: <code>{user_id}</code>\n\n"
                f"<i>Approved by {callback_query.from_user.mention}</i>",
                parse_mode=enums.ParseMode.HTML
            )
            await callback_query.answer("✅ User approved!")
        except Exception as e:
            await callback_query.answer(f"❌ Failed: {e}", show_alert=True)


    # ==========================================================
    # Decline callback
    # ==========================================================

    @app.on_callback_query(filters.regex(r"^jr_decline_(-?\d+)_(\d+)$"))
    async def jr_decline_callback(client, callback_query):
        chat_id = int(callback_query.matches[0].group(1))
        user_id = int(callback_query.matches[0].group(2))

        # Only admins can decline
        if not await is_power(client, chat_id, callback_query.from_user.id):
            return await callback_query.answer("❌ Only admins can decline.", show_alert=True)

        try:
            await client.decline_chat_join_request(chat_id, user_id)
            user = await client.get_users(user_id)
            await callback_query.message.edit_text(
                f"❌ <b>Declined!</b>\n\n"
                f":⧽ 𝑛𝑎𝑚𝑒: <b>{user.first_name}</b>\n"
                f":⧽ 𝑖𝑑: <code>{user_id}</code>\n\n"
                f"<i>Declined by {callback_query.from_user.mention}</i>",
                parse_mode=enums.ParseMode.HTML
            )
            await callback_query.answer("❌ User declined.")
        except Exception as e:
            await callback_query.answer(f"❌ Failed: {e}", show_alert=True)
