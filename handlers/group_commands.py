# ============================================================
# Group Manager Bot — 
# Author: Mr. Stark
# ============================================================

from pyrogram import Client, filters
from pyrogram.types import Message, ChatMemberUpdated, ChatPermissions, ChatPrivileges
from pyrogram.enums import ChatMemberStatus
from pyrogram.raw import functions, types as raw_types
import re
import logging
import db

DEFAULT_WELCOME = "👋 Welcome {first_name} to {title}!"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Link patterns for biolink detection
URL_PATTERN = re.compile(
    r"(https?://[^\s]+|www\.[^\s]+|t\.me/[^\s]+)",
    re.IGNORECASE
)


# ==========================================================
# Global helpers
# ==========================================================

async def is_power(client, chat_id: int, user_id: int) -> bool:
    member = await client.get_chat_member(chat_id, user_id)
    return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]


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


async def handle_welcome(client, chat_id: int, users: list, chat_title: str):
    status = await db.get_welcome_status(chat_id)
    if not status:
        return

    welcome_text = await db.get_welcome_message(chat_id) or DEFAULT_WELCOME

    for user in users:
        try:
            text = welcome_text.format(
                username=user.username or user.first_name,
                first_name=user.first_name,
                mention=f"[{user.first_name}](tg://user?id={user.id})",
                title=chat_title,
            )
        except KeyError:
            text = DEFAULT_WELCOME.format(first_name=user.first_name, title=chat_title)

        try:
            await client.send_message(chat_id, text)
        except Exception as e:
            logger.error(f"🚨 Failed to send welcome message: {e}")


async def user_has_bio_link(client, user_id: int) -> bool:
    """Raw MTProto se user ki actual bio fetch karo aur links check karo"""
    try:
        input_user = await client.resolve_peer(user_id)
        full = await client.invoke(
            functions.users.GetFullUser(id=input_user)
        )
        bio = ""
        if hasattr(full, "full_user") and full.full_user:
            bio = getattr(full.full_user, "about", None) or ""
        elif hasattr(full, "about"):
            bio = getattr(full, "about", None) or ""

        if not bio:
            return False

        if URL_PATTERN.search(bio):
            return True
        if "t.me/" in bio.lower() or "http" in bio.lower() or "www." in bio.lower():
            return True

    except Exception as e:
        logger.error(f"Bio check error for {user_id}: {e}")
    return False


def register_group_commands(app: Client):

    # ==========================================================
    # Welcome event
    # ==========================================================

    @app.on_chat_member_updated()
    async def member_update(client: Client, cmu: ChatMemberUpdated):
        if not cmu.new_chat_member:
            return

        user = cmu.new_chat_member.user
        new_status = cmu.new_chat_member.status

        if new_status == ChatMemberStatus.MEMBER:
            await handle_welcome(
                client,
                cmu.chat.id,
                [user],
                cmu.chat.title,
            )


    # ==========================================================
    # Welcome toggle
    # ==========================================================

    @app.on_message(filters.group & filters.command("welcome"))
    async def welcome_toggle(client, message: Message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Only admin or owner can use this command.")

        parts = message.text.split(maxsplit=1)
        if len(parts) < 2 or parts[1].lower() not in ["on", "off"]:
            return await message.reply_text("⚙️ Usage: /welcome on/off")

        status = parts[1].lower() == "on"
        await db.set_welcome_status(message.chat.id, status)

        await message.reply_text(
            "✅ Welcome messages ON." if status else "⚠️ Welcome messages OFF."
        )


    # ==========================================================
    # Set welcome
    # ==========================================================

    @app.on_message(filters.group & filters.command("setwelcome"))
    async def set_welcome(client, message: Message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("⚠️ Only admin can use this command.")

        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            return await message.reply_text("🤖 Usage: /setwelcome <message>")

        await db.set_welcome_message(message.chat.id, parts[1])
        await message.reply_text("✅ Custom welcome saved!")


    # ==========================================================
    # Lock
    # ==========================================================

    VALID_LOCKS = ["url", "sticker", "media", "username", "forward", "text", "edit"]

    @app.on_message(filters.group & filters.command("lock"))
    async def lock_command(client, message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Only admin can use this command.")

        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            return await message.reply_text(f"⚙️ Usage: /lock <type>\n\nAvailable: {', '.join(VALID_LOCKS)}")

        lock_type = parts[1].lower()

        if lock_type not in VALID_LOCKS:
            return await message.reply_text(f"⚠️ Available locks:\n{', '.join(VALID_LOCKS)}")

        await db.set_lock(message.chat.id, lock_type, True)
        await message.reply_text(f"🔒 `{lock_type}` lock enabled!")


    # ==========================================================
    # Unlock
    # ==========================================================

    @app.on_message(filters.group & filters.command("unlock"))
    async def unlock_command(client, message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Only admin can use this command.")

        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            return await message.reply_text(f"⚙️ Usage: /unlock <type>\n\nAvailable: {', '.join(VALID_LOCKS)}")

        lock_type = parts[1].lower()

        if lock_type not in VALID_LOCKS:
            return await message.reply_text(f"⚠️ Available locks:\n{', '.join(VALID_LOCKS)}")

        await db.set_lock(message.chat.id, lock_type, False)
        await message.reply_text(f"🔓 `{lock_type}` lock disabled!")


    # ==========================================================
    # Locks list
    # ==========================================================

    @app.on_message(filters.group & filters.command("locks"))
    async def locks_list(client, message):
        locks = await db.get_locks(message.chat.id)
        if not locks:
            return await message.reply_text("🤖 No locks configured yet.")

        text = "🔐 **Active Locks:**\n\n"
        for k, v in locks.items():
            text += f"• `{k}`: {'🔒 ON' if v else '🔓 OFF'}\n"

        await message.reply_text(text)


    # ==========================================================
    # lockall
    # ==========================================================

    @app.on_message(filters.group & filters.command("lockall"))
    async def lockall_command(client, message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Only admin can use this command.")

        for lock_type in VALID_LOCKS:
            await db.set_lock(message.chat.id, lock_type, True)

        locked_list = "\n".join(f"🔒 `{l}`" for l in VALID_LOCKS)
        await message.reply_text(f"🔐 **Everything Locked !**\n\n{locked_list}")


    # ==========================================================
    # unlockall
    # ==========================================================

    @app.on_message(filters.group & filters.command("unlockall"))
    async def unlockall_command(client, message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Only admin can use this command.")

        for lock_type in VALID_LOCKS:
            await db.set_lock(message.chat.id, lock_type, False)

        await message.reply_text("🔓 **Everyone's locks are OFF! **\n\nNow everything is allowed in the group.")

    

    # ==========================================================
    # Enforce locks — messages (text, url, sticker, media, username, forward, text)
    # ==========================================================

    @app.on_message(filters.group & ~filters.service, group=1)
    async def enforce_locks(client, message):
        try:
            member = await client.get_chat_member(message.chat.id, message.from_user.id)
            if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                return
        except:
            return

        locks = await db.get_locks(message.chat.id)
        if not locks:
            return

        # 🔇 Text lock — koi bhi text message delete hoga
        if locks.get("text") and message.text and not message.sticker:
            return await message.delete()

        # 🔗 URL lock
        if locks.get("url") and message.text:
            if message.entities:
                for ent in message.entities:
                    if ent.type.name in ["URL", "TEXT_LINK"]:
                        return await message.delete()
            if "t.me/" in message.text.lower() or "http" in message.text.lower():
                return await message.delete()

        # 🎭 Sticker lock
        if locks.get("sticker") and message.sticker:
            return await message.delete()

        # 🖼️ Media lock
        if locks.get("media") and (message.photo or message.video or message.document or message.audio or message.animation):
            return await message.delete()

        # 👤 Username mention lock
        if locks.get("username") and message.text and "@" in message.text:
            return await message.delete()

        # ↩️ Forward lock
        if locks.get("forward") and message.forward_from:
            return await message.delete()

        # 🔗 BioLink check — agar biolink ON hai
        biolink_on = await db.get_biolink_status(message.chat.id)
        if biolink_on:
            has_link = await user_has_bio_link(client, message.from_user.id)
            if has_link:
                try:
                    await message.delete()
                    await client.send_message(
                        message.chat.id,
                        f"⛔ {message.from_user.mention}, Your message was deleted because of the link in the bio..\n\n"
                        f"✅ First remove the link from your bio, then message.",
                    )
                except Exception as e:
                    logger.error(f"BioLink enforce error: {e}")
                return


    # ==========================================================
    # Enforce edit lock — edited messages
    # ==========================================================

    @app.on_edited_message(filters.group, group=1)
    async def enforce_edit_lock(client, message):
        try:
            member = await client.get_chat_member(message.chat.id, message.from_user.id)
            if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                return
        except:
            return

        locks = await db.get_locks(message.chat.id)
        if locks.get("edit"):
            try:
                await message.delete()
            except Exception as e:
                logger.error(f"Edit lock error: {e}")


    # ==========================================================
    # BioLink toggle
    # ==========================================================

    @app.on_message(filters.group & filters.command("biolink"))
    async def biolink_toggle(client, message: Message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Only admin or owner can use this command.")

        parts = message.text.split(maxsplit=1)
        if len(parts) < 2 or parts[1].lower() not in ["on", "off"]:
            status = await db.get_biolink_status(message.chat.id)
            current = "🟢 ON" if status else "🔴 OFF"
            return await message.reply_text(
                f"⚙️ Usage: `/biolink on` ya `/biolink off`\n\n"
                f"📊 Current Status: {current}"
            )

        status = parts[1].lower() == "on"
        await db.set_biolink_status(message.chat.id, status)

        if status:
            await message.reply_text(
                "✅ **BioLink Protection ON!**\n\n"
                "Now, the messages of those users who have a link in their bio will be automatically deleted.. 🔗🚫"
            )
        else:
            await message.reply_text(
                "⚠️ **BioLink Protection OFF!**\n\n"
                "👀 Now users with link in bio can also message."
            )


    # ==========================================================
    # Kick
    # ==========================================================

    @app.on_message(filters.group & filters.command("kick"))
    async def kick_user(client, message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Only admin can use this command.")

        user = await extract_target_user(client, message)
        if not user:
            return await message.reply_text("⚠️ Usage: Reply or use `/kick @username`")

        target_member = await client.get_chat_member(message.chat.id, user.id)
        if target_member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return await message.reply_text("⚠️ Cannot perform action on admins.")
        if user.id == message.from_user.id:
            return await message.reply_text("⚠️ You cannot kick yourself.")

        try:
            await client.ban_chat_member(message.chat.id, user.id)
            await client.unban_chat_member(message.chat.id, user.id)
            await message.reply_text(f"👢 {user.mention} has been kicked.")
        except Exception as e:
            await message.reply_text(f"❌ Failed to kick: {e}")


    # ==========================================================
    # Ban
    # ==========================================================

    @app.on_message(filters.group & filters.command("ban"))
    async def ban_user(client, message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Only admin can use this command.")

        user = await extract_target_user(client, message)
        if not user:
            return await message.reply_text("⚠️ Usage: Reply or use `/ban @username`")

        target_member = await client.get_chat_member(message.chat.id, user.id)
        if target_member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return await message.reply_text("⚠️ Cannot perform action on admins.")
        if user.id == message.from_user.id:
            return await message.reply_text("⚠️ You cannot ban yourself.")

        try:
            await client.ban_chat_member(message.chat.id, user.id)
            await message.reply_text(f"🚨 {user.mention} has been banned.")
        except Exception as e:
            await message.reply_text(f"❌ Failed to ban: {e}")


    # ==========================================================
    # Unban
    # ==========================================================

    @app.on_message(filters.group & filters.command("unban"))
    async def unban_user(client, message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Only admin can use this command.")

        user = await extract_target_user(client, message)
        if not user:
            return await message.reply_text("⚠️ Usage: Reply or use `/unban @username`")

        target_member = await client.get_chat_member(message.chat.id, user.id)
        if target_member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return await message.reply_text("⚠️ Cannot perform action on admins.")
        if user.id == message.from_user.id:
            return await message.reply_text("⚠️ You cannot unban yourself.")

        try:
            await client.unban_chat_member(message.chat.id, user.id)
            await message.reply_text(f"✅ {user.mention} has been unbanned.")
        except Exception as e:
            await message.reply_text(f"❌ Failed to unban: {e}")


    # ==========================================================
    # Mute
    # ==========================================================

    @app.on_message(filters.group & filters.command("mute"))
    async def mute_user(client, message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Only admin can use this command.")

        user = await extract_target_user(client, message)
        if not user:
            return await message.reply_text("⚠️ Usage: Reply or use `/mute @username`")

        target_member = await client.get_chat_member(message.chat.id, user.id)
        if target_member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return await message.reply_text("⚠️ Cannot perform action on admins.")
        if user.id == message.from_user.id:
            return await message.reply_text("⚠️ You cannot mute yourself.")

        try:
            await client.restrict_chat_member(
                message.chat.id,
                user.id,
                permissions=ChatPermissions(can_send_messages=False),
            )
            await message.reply_text(f"🔇 {user.mention} has been muted.")
        except Exception as e:
            await message.reply_text(f"❌ Failed to mute: {e}")


    # ==========================================================
    # Unmute
    # ==========================================================

    @app.on_message(filters.group & filters.command("unmute"))
    async def unmute_user(client, message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Only admin can use this command.")

        user = await extract_target_user(client, message)
        if not user:
            return await message.reply_text("⚠️ Usage: Reply or use `/unmute @username`")

        target_member = await client.get_chat_member(message.chat.id, user.id)
        if target_member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return await message.reply_text("⚠️ Cannot perform action on admins.")
        if user.id == message.from_user.id:
            return await message.reply_text("⚠️ You cannot unmute yourself.")

        try:
            await client.restrict_chat_member(
                message.chat.id,
                user.id,
                permissions=ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True,
                ),
            )
            await message.reply_text(f"🔊 {user.mention} has been unmuted.")
        except Exception as e:
            await message.reply_text(f"❌ Failed to unmute: {e}")



    # ==========================================================
# tmute
# ==========================================================

    @app.on_message(filters.group & filters.command("tmute"))
    async def tmute_user(client, message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Only admins can use this command.")

        parts = message.text.split(maxsplit=2)
        if len(parts) < 3 and not message.reply_to_message:
            return await message.reply_text("⚙️ Usage: `/tmute @user 10m` or reply with `/tmute 10m`")

        if message.reply_to_message:
            user = message.reply_to_message.from_user
            time_arg = parts[1] if len(parts) > 1 else None
        else:
            user = await extract_target_user(client, message)
            time_arg = parts[2] if len(parts) > 2 else None

        if not user or not time_arg:
            return await message.reply_text("⚙️ Usage: `/tmute @user 10m` or reply with `/tmute 10m`")

        match = re.fullmatch(r"(\d+)(m|h)", time_arg.strip().lower())
        if not match:
            return await message.reply_text("⚠️ Invalid time! Use: `10m` `1h` `12h` `24h`")

        value, unit = int(match.group(1)), match.group(2)
        seconds = value * 60 if unit == "m" else value * 3600
        if seconds < 60 or seconds > 86400:
            return await message.reply_text("⚠️ Time must be between 1m and 24h.")

        target = await client.get_chat_member(message.chat.id, user.id)
        if target.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return await message.reply_text("⚠️ Cannot mute an admin.")

        from datetime import datetime, timedelta
        until = datetime.utcnow() + timedelta(seconds=seconds)

        try:
            await client.restrict_chat_member(
                message.chat.id,
                user.id,
                permissions=ChatPermissions(can_send_messages=False),
                until_date=until
            )
            await message.reply_text(f"🔇 {user.mention} muted for `{time_arg}`.")
        except Exception as e:
            await message.reply_text(f"❌ Failed: {e}")
 

# ==========================================================
# tban
# ==========================================================

    @app.on_message(filters.group & filters.command("tban"))
    async def tban_user(client, message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Only admins can use this command.")

        parts = message.text.split(maxsplit=2)
        if len(parts) < 3 and not message.reply_to_message:
            return await message.reply_text("⚙️ Usage: `/tban @user 10m` or reply with `/tban 10m`")

        if message.reply_to_message:
            user = message.reply_to_message.from_user
            time_arg = parts[1] if len(parts) > 1 else None
        else:
            user = await extract_target_user(client, message)
            time_arg = parts[2] if len(parts) > 2 else None

        if not user or not time_arg:
            return await message.reply_text("⚙️ Usage: `/tban @user 10m` or reply with `/tban 10m`")

        match = re.fullmatch(r"(\d+)(m|h)", time_arg.strip().lower())
        if not match:
            return await message.reply_text("⚠️ Invalid time! Use: `10m` `1h` `12h` `24h`")

        value, unit = int(match.group(1)), match.group(2)
        seconds = value * 60 if unit == "m" else value * 3600
        if seconds < 60 or seconds > 86400:
            return await message.reply_text("⚠️ Time must be between 1m and 24h.")

        target = await client.get_chat_member(message.chat.id, user.id)
        if target.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return await message.reply_text("⚠️ Cannot ban an admin.")

        from datetime import datetime, timedelta
        until = datetime.utcnow() + timedelta(seconds=seconds)

        try:
            await client.ban_chat_member(
                message.chat.id,
                user.id,
                until_date=until
            )
            await message.reply_text(f"🚨 {user.mention} banned for `{time_arg}`.")
        except Exception as e:
            await message.reply_text(f"❌ Failed: {e}")

    # ==========================================================
    # Warn
    # ==========================================================

    @app.on_message(filters.group & filters.command("warn"))
    async def warn_user(client, message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Only admin can use this command.")

        user = await extract_target_user(client, message)
        if not user:
            return await message.reply_text("⚠️ Usage: Reply or use `/warn @username`")

        target_member = await client.get_chat_member(message.chat.id, user.id)
        if target_member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return await message.reply_text("⚠️ Cannot warn admins.")
        if user.id == message.from_user.id:
            return await message.reply_text("⚠️ You cannot warn yourself.")

        warns = await db.add_warn(message.chat.id, user.id)
        if warns >= 3:
            await client.restrict_chat_member(
                message.chat.id,
                user.id,
                permissions=ChatPermissions(can_send_messages=False),
            )
            await message.reply_text(f"🚫 {user.mention} reached 3 warns and was muted.")
        else:
            await message.reply_text(f"⚠️ {user.mention} now has {warns}/3 warnings.")


    # ==========================================================
    # Warns
    # ==========================================================

    @app.on_message(filters.group & filters.command("warns"))
    async def warns_user(client, message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Only admin can use this command.")

        user = await extract_target_user(client, message)
        if not user:
            return await message.reply_text("⚠️ Usage: Reply or use `/warns @username`")

        target_member = await client.get_chat_member(message.chat.id, user.id)
        if target_member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return await message.reply_text("⚠️ Cannot check warns for admins.")

        warns = await db.get_warns(message.chat.id, user.id)
        await message.reply_text(f"⚠️ {user.mention} has {warns}/3 warnings.")


    # ==========================================================
    # Resetwarns
    # ==========================================================

    @app.on_message(filters.group & filters.command("resetwarns"))
    async def resetwarns_user(client, message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Only admin can use this command.")

        user = await extract_target_user(client, message)
        if not user:
            return await message.reply_text("⚠️ Usage: Reply or use `/resetwarns @username`")

        target_member = await client.get_chat_member(message.chat.id, user.id)
        if target_member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return await message.reply_text("⚠️ Cannot reset warns for admins.")

        await db.reset_warns(message.chat.id, user.id)
        await message.reply_text(f"✅ {user.mention}'s warns have been reset.")


    # ==========================================================
    # Promote
    # ==========================================================

    @app.on_message(filters.group & filters.command("promote"))
    async def promote_user(client: Client, message: Message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Only admin or owner can use this command.")

        user = await extract_target_user(client, message)
        if not user:
            return await message.reply_text("⚠️ Usage: Reply to a user or use '/promote @username'")

        target_member = await client.get_chat_member(message.chat.id, user.id)

        if target_member.status == ChatMemberStatus.OWNER:
            return await message.reply_text("⚠️ Cannot promote the group owner.")
        if user.id == message.from_user.id:
            return await message.reply_text("⚠️ You cannot promote yourself.")

        try:
            privileges = ChatPrivileges(
                can_manage_chat=True,
                can_delete_messages=True,
                can_manage_video_chats=True,
                can_restrict_members=True,
                can_promote_members=False,
                can_change_info=True,
                can_invite_users=True,
                can_pin_messages=True,
                can_post_messages=False,
                can_edit_messages=False,
                is_anonymous=False
            )

            await client.promote_chat_member(
                chat_id=message.chat.id,
                user_id=user.id,
                privileges=privileges
            )
            await message.reply_text(f"✅ {user.mention} has been promoted to admin.")

        except Exception as e:
            if "USER_NOT_PARTICIPANT" in str(e):
                await message.reply_text("⚠️ Cannot promote: user is not a member of this chat.")
            elif "CHAT_ADMIN_REQUIRED" in str(e):
                await message.reply_text("⚠️ Bot must be admin with 'Add Admins' permission to promote.")
            else:
                await message.reply_text(f"❌ Failed to promote: {e}")


    # ==========================================================
    # Demote
    # ==========================================================

    @app.on_message(filters.group & filters.command("demote"))
    async def demote_user(client: Client, message: Message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Only admin can use this command.")

        user = await extract_target_user(client, message)
        if not user:
            return await message.reply_text("⚠️ Usage: Reply to a user or use '/demote @username'")

        try:
            target_member = await client.get_chat_member(message.chat.id, user.id)
        except Exception as e:
            if "USER_NOT_PARTICIPANT" in str(e):
                return await message.reply_text("❌ Cannot demote: user is not a member of this chat.")
            return await message.reply_text(f"⚠️ Failed to demote: {e}")

        if target_member.status == ChatMemberStatus.OWNER:
            return await message.reply_text("⚠️ You cannot demote the group owner.")
        if target_member.status not in [ChatMemberStatus.ADMINISTRATOR]:
            return await message.reply_text("⚠️ User is not an admin.")
        if user.id == message.from_user.id:
            return await message.reply_text("❌ You cannot demote yourself.")

        try:
            no_privileges = ChatPrivileges(
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

            await client.promote_chat_member(
                chat_id=message.chat.id,
                user_id=user.id,
                privileges=no_privileges
            )
            await message.reply_text(f"✅ {user.mention} has been demoted from admin.")

        except Exception as e:
            if "CHAT_ADMIN_REQUIRED" in str(e):
                await message.reply_text("❌ Bot must be admin with 'Add Admins' permission to demote.")
            else:
                await message.reply_text(f"⚠️ Failed to demote: {e}")
