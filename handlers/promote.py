# ============================================================
# Group Manager Bot — Promote & Demote
# Author: Mr. Stark
# ============================================================

from pyrogram import Client, filters, enums
from pyrogram.types import Message, ChatPrivileges
from pyrogram.errors import ChatAdminRequired
from pyrogram.enums import ChatMemberStatus
import logging

logger = logging.getLogger(__name__)


# ==========================================================
# Mention helper
# ==========================================================

def mention(user_id, name):
    return f"[{name}](tg://user?id={user_id})"


# ==========================================================
# Extract user and optional title
# ==========================================================

async def extract_user_and_title(message, client):
    user = None

    cmd = message.text.strip().split()[0]
    text = message.text[len(cmd):].strip()

    if message.reply_to_message:
        user = message.reply_to_message.from_user
        if not user:
            await message.reply_text("❌ Cannot find the user in the replied message.")
            return None, None, None
        title = text if text else None
    else:
        args = text.strip().split(maxsplit=1)
        if not args:
            await message.reply_text("⚙️ Please specify a user or reply to a message.")
            return None, None, None
        user_arg = args[0]
        try:
            user = await client.get_users(user_arg)
            if not user:
                await message.reply_text("❌ Cannot find that user.")
                return None, None, None
        except Exception:
            await message.reply_text("❌ Cannot find that user.")
            return None, None, None
        title = args[1] if len(args) > 1 else None

    return user.id, user.first_name, title


# ==========================================================
# Admin permission check
# ==========================================================

async def check_admin(client, message, *privileges):
    if not message.from_user:
        await message.reply_text("❌ Anonymous admins cannot use this command.")
        return False

    member = await message.chat.get_member(message.from_user.id)

    if member.status == enums.ChatMemberStatus.OWNER:
        return True

    if member.status == enums.ChatMemberStatus.ADMINISTRATOR:
        if not member.privileges:
            await message.reply_text("❌ Cannot retrieve your admin privileges.")
            return False
        missing = [p for p in privileges if not getattr(member.privileges, p, False)]
        if missing:
            await message.reply_text(f"❌ You don't have required permission: `{', '.join(missing)}`")
            return False
        return True

    await message.reply_text("❌ You are not an admin.")
    return False


# ==========================================================
# Format message
# ==========================================================

def format_msg(chat_name, user_mention, admin_mention, action):
    action_text = "Promoting" if action == "promote" else "Demoting"
    return (
        f"» **{action_text}** a user in {chat_name}\n"
        f"**User :** {user_mention}\n"
        f"**Admin :** {admin_mention}"
    )


# ==========================================================
# Help Text
# ==========================================================
PROMOTE_HELP_TEXT = """
<b>╔══════════════════╗</b>
<b>   👮 ᴘʀᴏᴍᴏᴛᴇ sʏsᴛᴇᴍ</b>
<b>╚══════════════════╝</b>

<b>❖ Three levels of promotion available:</b>

❍ /promote <code>{user}</code><blockquote expandable><b>
➻ sᴛᴀɴᴅᴀʀᴅ ᴀᴅᴍɪɴ  
➥ ᴅᴇʟᴇᴛᴇ ᴍᴇssᴀɢᴇs  
➥ ɪɴᴠɪᴛᴇ ᴠɪᴀ ʟɪɴᴋ  
➥ ᴘɪɴ ᴍᴇssᴀɢᴇs  
➥ ᴇᴅɪᴛ ᴍᴇssᴀɢᴇs  
➥ ᴍᴀɴᴀɢᴇ ʟɪᴠᴇ sᴛʀᴇᴀᴍs  
➥ ᴍᴀɴᴀɢᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛs  
</b></blockquote>
❍ /mod <code>{user}</code><blockquote expandable><b>
➻ ᴍᴏᴅᴇʀᴀᴛᴏʀ  
➥ ᴅᴇʟᴇᴛᴇ ᴍᴇssᴀɢᴇs  
➥ ᴍᴀɴᴀɢᴇ ᴍᴇssᴀɢᴇs  
➥ ᴍᴀɴᴀɢᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛs  
➥ ᴍᴀɴᴀɢᴇ ʟɪᴠᴇ sᴛʀᴇᴀᴍs  
</b></blockquote>
❍ /fullpromote <code>{user}</code> <blockquote expandable><b>
➻ ғᴜʟʟ ᴀᴅᴍɪɴ (ᴀʟʟ ᴘᴏᴡᴇʀs)  
➥ ᴀʟʟ ᴘᴇʀᴍɪssɪᴏɴs ᴇxᴄᴇᴘᴛ ᴀɴᴏɴʏᴍᴏᴜs  
</b></blockquote>

❍ /demote <code>{user}</code> <blockquote expandable><b>➥ ʀᴇᴍᴏᴠᴇ ᴀᴅᴍɪɴ ʀɪɢʜᴛs</b></blockquote>

<b>👮 Only admins can use these commands.</b>
"""

def register_promote_handler(app: Client):

    # ==========================================================
    # /promote — Standard admin
    # ==========================================================

    @app.on_message(filters.group & filters.command("promote"))
    async def promote_cmd(client, message: Message):
        if not await check_admin(client, message, "can_promote_members"):
            return

        user_id, first_name, title = await extract_user_and_title(message, client)
        if not user_id:
            return

        try:
            member = await client.get_chat_member(message.chat.id, user_id)
            if member.status == enums.ChatMemberStatus.ADMINISTRATOR:
                return await message.reply_text("⚠️ This user is already an admin.")

            await client.promote_chat_member(
                chat_id=message.chat.id,
                user_id=user_id,
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
                    can_edit_messages=False,
                    is_anonymous=False
                )
            )

            if title:
                try:
                    await client.set_administrator_title(message.chat.id, user_id, title)
                except Exception as e:
                    await message.reply_text(f"⚠️ Title set failed: {e}")

            await message.reply_text(
                format_msg(
                    message.chat.title,
                    mention(user_id, first_name),
                    mention(message.from_user.id, message.from_user.first_name),
                    "promote"
                ) + "\n\n✅ Promoted as **Admin**."
            )

        except ChatAdminRequired:
            await message.reply_text("❌ I need admin with promote permissions.")
        except Exception as e:
            await message.reply_text(f"❌ Failed: {e}")


    # ==========================================================
    # /mod — Moderator
    # ==========================================================

    @app.on_message(filters.group & filters.command("mod"))
    async def mod_cmd(client, message: Message):
        if not await check_admin(client, message, "can_promote_members"):
            return

        user_id, first_name, title = await extract_user_and_title(message, client)
        if not user_id:
            return

        try:
            member = await client.get_chat_member(message.chat.id, user_id)
            if member.status == enums.ChatMemberStatus.ADMINISTRATOR:
                return await message.reply_text("⚠️ This user is already an admin.")

            await client.promote_chat_member(
                chat_id=message.chat.id,
                user_id=user_id,
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

            if title:
                try:
                    await client.set_administrator_title(message.chat.id, user_id, title)
                except Exception as e:
                    await message.reply_text(f"⚠️ Title set failed: {e}")

            await message.reply_text(
                format_msg(
                    message.chat.title,
                    mention(user_id, first_name),
                    mention(message.from_user.id, message.from_user.first_name),
                    "promote"
                ) + "\n\n✅ Promoted as **Moderator**."
            )

        except ChatAdminRequired:
            await message.reply_text("❌ I need admin with promote permissions.")
        except Exception as e:
            await message.reply_text(f"❌ Failed: {e}")


    # ==========================================================
    # /fullpromote — Full admin except anonymous
    # ==========================================================

    @app.on_message(filters.group & filters.command("fullpromote"))
    async def fullpromote_cmd(client, message: Message):
        if not await check_admin(client, message, "can_promote_members"):
            return

        user_id, first_name, title = await extract_user_and_title(message, client)
        if not user_id:
            return

        try:
            member = await client.get_chat_member(message.chat.id, user_id)
            if member.status == enums.ChatMemberStatus.ADMINISTRATOR:
                return await message.reply_text("⚠️ This user is already an admin.")

            await client.promote_chat_member(
                chat_id=message.chat.id,
                user_id=user_id,
                privileges=ChatPrivileges(
                    can_manage_chat=True,
                    can_change_info=True,
                    can_delete_messages=True,
                    can_invite_users=True,
                    can_restrict_members=True,
                    can_pin_messages=True,
                    can_promote_members=True,
                    can_manage_video_chats=True,
                    is_anonymous=False
                )
            )

            if title:
                try:
                    await client.set_administrator_title(message.chat.id, user_id, title)
                except Exception as e:
                    await message.reply_text(f"⚠️ Title set failed: {e}")

            await message.reply_text(
                format_msg(
                    message.chat.title,
                    mention(user_id, first_name),
                    mention(message.from_user.id, message.from_user.first_name),
                    "promote"
                ) + "\n\n✅ Promoted as **Full Admin**."
            )

        except ChatAdminRequired:
            await message.reply_text("❌ I need admin with promote permissions.")
        except Exception as e:
            await message.reply_text(f"❌ Failed: {e}")


    # ==========================================================
    # /demote
    # ==========================================================

    @app.on_message(filters.group & filters.command("demote"))
    async def demote_cmd(client, message: Message):
        if not await check_admin(client, message, "can_promote_members"):
            return

        user_id, first_name, _ = await extract_user_and_title(message, client)
        if not user_id:
            return

        try:
            member = await client.get_chat_member(message.chat.id, user_id)
            if member.status != enums.ChatMemberStatus.ADMINISTRATOR:
                return await message.reply_text("⚠️ This user is not an admin.")
            if member.status == enums.ChatMemberStatus.OWNER:
                return await message.reply_text("⚠️ Cannot demote the group owner.")

            await client.promote_chat_member(
                chat_id=message.chat.id,
                user_id=user_id,
                privileges=ChatPrivileges(
                    can_manage_chat=False,
                    can_change_info=False,
                    can_delete_messages=False,
                    can_invite_users=False,
                    can_restrict_members=False,
                    can_pin_messages=False,
                    can_promote_members=False,
                    can_manage_video_chats=False,
                    is_anonymous=False
                )
            )

            await message.reply_text(
                format_msg(
                    message.chat.title,
                    mention(user_id, first_name),
                    mention(message.from_user.id, message.from_user.first_name),
                    "demote"
                ) + "\n\n✅ Demoted successfully."
            )

        except ChatAdminRequired:
            await message.reply_text("❌ I need admin with promote permissions.")
        except Exception as e:
            if "CHAT_ADMIN_REQUIRED" in str(e):
                await message.reply_text("❌ I don't have permission to demote this user.")
            else:
                await message.reply_text(f"❌ Failed: {e}")
