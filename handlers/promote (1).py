# ============================================================
# Group Manager Bot — Promote & Demote
# Author: Mr. Stark
# ============================================================

from pyrogram import Client, filters
from pyrogram.types import Message, ChatPrivileges
from pyrogram.enums import ChatMemberStatus
import logging

logger = logging.getLogger(__name__)


async def can_promote(client, chat_id: int, user_id: int) -> bool:
    member = await client.get_chat_member(chat_id, user_id)
    if member.status == ChatMemberStatus.OWNER:
        return True
    if member.status == ChatMemberStatus.ADMINISTRATOR:
        return bool(member.privileges.can_promote_members)
    return False


async def extract_target_user(client, message):
    if message.reply_to_message:
        return message.reply_to_message.from_user
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return None
    arg = parts[1]
    try:
        if arg.startswith("@"):
            return await client.get_users(arg)
        elif arg.isdigit():
            return await client.get_users(int(arg))
    except:
        return None


# ==========================================================
# Help Text
# ==========================================================

PROMOTE_HELP_TEXT = """
╔══════════════════╗
   👮 PROMOTE SYSTEM
╚══════════════════╝

Three levels of promotion available:

• /promote <user>
  → Standard admin
  - Delete messages
  - Invite via link
  - Pin messages
  - Edit messages
  - Manage live streams
  - Manage voice chats

• /mod <user>
  → Moderator
  - Delete messages
  - Manage messages
  - Manage voice chats
  - Manage live streams

• /fullpromote <user>
  → Full admin (all powers)
  - All permissions except anonymous

• /demote <user>
  → Remove all admin rights

👮 Only admins with Add Admin
   permission can use these commands.
"""


def register_promote_handler(app: Client):

    # ==========================================================
    # /promote — Standard admin
    # ==========================================================

    @app.on_message(filters.group & filters.command("promote"))
    async def promote_cmd(client, message: Message):
        if not await can_promote(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ You don't have permission to add admins.")

        user = await extract_target_user(client, message)
        if not user:
            return await message.reply_text("⚙️ Usage: Reply or use `/promote @username`")

        target = await client.get_chat_member(message.chat.id, user.id)
        if target.status == ChatMemberStatus.OWNER:
            return await message.reply_text("⚠️ Cannot promote the group owner.")
        if user.id == message.from_user.id:
            return await message.reply_text("⚠️ You cannot promote yourself.")

        try:
            await client.promote_chat_member(
                chat_id=message.chat.id,
                user_id=user.id,
                privileges=ChatPrivileges(
                    can_manage_chat=True,
                    can_delete_messages=True,
                    can_manage_video_chats=True,
                    can_restrict_members=False,
                    can_promote_members=False,
                    can_change_info=False,
                    can_invite_users=True,
                    can_pin_messages=True,
                    can_post_messages=False,
                    can_edit_messages=True,
                    is_anonymous=False
                )
            )
            await message.reply_text(
                f"✅ {user.mention} promoted as **Admin**.\n\n"
                f"Powers: Delete messages, Invite link, "
                f"Pin messages, Edit messages, Live streams, Voice chats."
            )
        except Exception as e:
            await message.reply_text(f"❌ Failed to promote: {e}")


    # ==========================================================
    # /mod — Moderator
    # ==========================================================

    @app.on_message(filters.group & filters.command("mod"))
    async def mod_cmd(client, message: Message):
        if not await can_promote(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ You don't have permission to add admins.")

        user = await extract_target_user(client, message)
        if not user:
            return await message.reply_text("⚙️ Usage: Reply or use `/mod @username`")

        target = await client.get_chat_member(message.chat.id, user.id)
        if target.status == ChatMemberStatus.OWNER:
            return await message.reply_text("⚠️ Cannot promote the group owner.")
        if user.id == message.from_user.id:
            return await message.reply_text("⚠️ You cannot promote yourself.")

        try:
            await client.promote_chat_member(
                chat_id=message.chat.id,
                user_id=user.id,
                privileges=ChatPrivileges(
                    can_manage_chat=True,
                    can_delete_messages=True,
                    can_manage_video_chats=True,
                    can_restrict_members=False,
                    can_promote_members=False,
                    can_change_info=False,
                    can_invite_users=False,
                    can_pin_messages=False,
                    can_post_messages=False,
                    can_edit_messages=False,
                    is_anonymous=False
                )
            )
            await message.reply_text(
                f"✅ {user.mention} promoted as **Moderator**.\n\n"
                f"Powers: Delete messages, Manage messages, "
                f"Voice chats, Live streams."
            )
        except Exception as e:
            await message.reply_text(f"❌ Failed to promote: {e}")


    # ==========================================================
    # /fullpromote — Full admin except anonymous
    # ==========================================================

    @app.on_message(filters.group & filters.command("fullpromote"))
    async def fullpromote_cmd(client, message: Message):
        if not await can_promote(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ You don't have permission to add admins.")

        user = await extract_target_user(client, message)
        if not user:
            return await message.reply_text("⚙️ Usage: Reply or use `/fullpromote @username`")

        target = await client.get_chat_member(message.chat.id, user.id)
        if target.status == ChatMemberStatus.OWNER:
            return await message.reply_text("⚠️ Cannot promote the group owner.")
        if user.id == message.from_user.id:
            return await message.reply_text("⚠️ You cannot promote yourself.")

        try:
            await client.promote_chat_member(
                chat_id=message.chat.id,
                user_id=user.id,
                privileges=ChatPrivileges(
                    can_manage_chat=True,
                    can_delete_messages=True,
                    can_manage_video_chats=True,
                    can_restrict_members=True,
                    can_promote_members=True,
                    can_change_info=True,
                    can_invite_users=True,
                    can_pin_messages=True,
                    can_post_messages=True,
                    can_edit_messages=True,
                    is_anonymous=False
                )
            )
            await message.reply_text(
                f"✅ {user.mention} promoted as **Full Admin**.\n\n"
                f"All powers granted except anonymous."
            )
        except Exception as e:
            await message.reply_text(f"❌ Failed to promote: {e}")


    # ==========================================================
    # /demote
    # ==========================================================

    @app.on_message(filters.group & filters.command("demote"))
    async def demote_cmd(client, message: Message):
        if not await can_promote(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ You don't have permission to demote admins.")

        user = await extract_target_user(client, message)
        if not user:
            return await message.reply_text("⚙️ Usage: Reply or use `/demote @username`")

        try:
            target = await client.get_chat_member(message.chat.id, user.id)
        except Exception as e:
            return await message.reply_text(f"⚠️ Failed: {e}")

        if target.status == ChatMemberStatus.OWNER:
            return await message.reply_text("⚠️ Cannot demote the group owner.")
        if target.status != ChatMemberStatus.ADMINISTRATOR:
            return await message.reply_text("⚠️ User is not an admin.")
        if user.id == message.from_user.id:
            return await message.reply_text("⚠️ You cannot demote yourself.")

        try:
            await client.promote_chat_member(
                chat_id=message.chat.id,
                user_id=user.id,
                privileges=ChatPrivileges(
                    can_manage_chat=False,
                    can_delete_messages=False,
                    can_manage_video_chats=False,
                    can_restrict_members=False,
                    can_promote_members=False,
                    can_change_info=False,
                    can_invite_users=False,
                    can_pin_messages=False,
                    can_post_messages=False,
                    can_edit_messages=False,
                    is_anonymous=False
                )
            )
            await message.reply_text(f"✅ {user.mention} has been demoted.")
        except Exception as e:
            await message.reply_text(f"❌ Failed to demote: {e}")
