# ============================================================
# Group Manager Bot
# Author: Mr. Stark
# ============================================================

from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto
)
from config import BOT_USERNAME, SUPPORT_GROUP, UPDATE_CHANNEL, START_IMAGE, OWNER_ID
import db


def register_handlers(app: Client):

    # ==========================================================
    # Start Message helper
    # ==========================================================
    async def send_start_menu(message, user):
        text = f"""

   ✨ Hello {user}! ✨

👋 I am Nomad 🤖 

Highlights:
─────────────────────────────
- Smart Anti-Spam & Link Shield
- Adaptive Lock System (URLs, Media, Text & more)
- BioLink Protection System
- Notes & Rules Management
- Modular & Scalable Protection
- Sleek UI with Inline Controls

» More New Features coming soon ...
"""
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("⚒️ Add to Group ⚒️", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
            [
                InlineKeyboardButton("⌂ Support ⌂", url=SUPPORT_GROUP),
                InlineKeyboardButton("⌂ Update ⌂", url=UPDATE_CHANNEL),
            ],
            [
                InlineKeyboardButton("※ ŎŴɳēŔ ※", url=f"tg://user?id={OWNER_ID}"),
                InlineKeyboardButton("Repo", url="https://github.com/LearningBotsOfficial/Nomade"),
            ],
            [InlineKeyboardButton("📚 Help Commands 📚", callback_data="help")]
        ])

        if message.text:
            await message.reply_photo(START_IMAGE, caption=text, reply_markup=buttons)
        else:
            media = InputMediaPhoto(media=START_IMAGE, caption=text)
            await message.edit_media(media=media, reply_markup=buttons)


    # ==========================================================
    # /start
    # ==========================================================
    @app.on_message(filters.private & filters.command("start"))
    async def start_command(client, message):
        args = message.text.split(maxsplit=1)

        if len(args) > 1 and args[1].startswith("note_"):
            payload = args[1]
            try:
                _, chat_id_str, name = payload.split("_", 2)
                chat_id = int(chat_id_str)
            except (ValueError, IndexError):
                return await message.reply_text("❌ Invalid note link.")

            content = await db.get_note(chat_id, name)
            if not content:
                return await message.reply_text(f"⚠️ Note `#{name}` not found or deleted.")

            return await message.reply_text(
                f"╔════════════════════════╗\n"
                f"   📝 Note: #{name}\n"
                f"╚════════════════════════╝\n\n"
                f"{content}"
            )

        user = message.from_user
        await db.add_user(user.id, user.first_name)
        await send_start_menu(message, user.first_name)


    # ==========================================================
    # Help Menu helper
    # ==========================================================
    async def send_help_menu(message):
        text = """
╔══════════════════╗
     Help Menu
╚══════════════════╝

Choose a category below to explore commands:
─────────────────────────────
"""
        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⌂ Greetings ⌂", callback_data="greetings"),
                InlineKeyboardButton("⌂ Locks ⌂", callback_data="locks"),
            ],
            [
                InlineKeyboardButton("⌂ Moderation ⌂", callback_data="moderation"),
                InlineKeyboardButton("🔗 BioLink", callback_data="biolink"),
            ],
            [
                InlineKeyboardButton("📝 Notes", callback_data="notes_help"),
                InlineKeyboardButton("📜 Rules", callback_data="rules_help"),
            ],
            [
                InlineKeyboardButton("🤬 Abuse", callback_data="abuse_help"),
                InlineKeyboardButton("📢 F-Sub", callback_data="fsub_help"),
            ],
            [
                InlineKeyboardButton("📢 Echo", callback_data="echo_help"),
                InlineKeyboardButton("📞 Phone", callback_data="phone_help"),
            ],
            [
                InlineKeyboardButton("📄 Long Limit", callback_data="longmsg_help"),
                InlineKeyboardButton("# Hashtag", callback_data="hashtag_help"),
            ],
            [
                InlineKeyboardButton("⚙️ Utility", callback_data="utility_help"),
                InlineKeyboardButton("🗑️ Cmd Deleter", callback_data="cmd_help"),
            ],
            [
                InlineKeyboardButton("🎬 Media Delete", callback_data="mediadelete_help"),
                InlineKeyboardButton("🧹 Cleaner", callback_data="cleaner_help"),
            ],
            [
                InlineKeyboardButton("🧟 Zombie", callback_data="zombie_help"),
                InlineKeyboardButton("📢 Tag All", callback_data="tagall_help"),
            ],
            [
                InlineKeyboardButton("👑 Promote", callback_data="promote_help"),
            ],
            [InlineKeyboardButton("🔙 Back", callback_data="back_to_start")]
        ])

        media = InputMediaPhoto(media=START_IMAGE, caption=text)
        await message.edit_media(media=media, reply_markup=buttons)


    # ==========================================================
    # help callback
    # ==========================================================
    @app.on_callback_query(filters.regex("^help$"))
    async def help_callback(client, callback_query):
        await send_help_menu(callback_query.message)
        await callback_query.answer()


    # ==========================================================
    # back_to_start callback
    # ==========================================================
    @app.on_callback_query(filters.regex("^back_to_start$"))
    async def back_to_start_callback(client, callback_query):
        user = callback_query.from_user.first_name
        await send_start_menu(callback_query.message, user)
        await callback_query.answer()


    # ==========================================================
    # Greetings callback
    # ==========================================================
    @app.on_callback_query(filters.regex("^greetings$"))
    async def greetings_callback(client, callback_query):
        text = """
╔══════════════════╗
    ⚙ Welcome System
╚══════════════════╝

Commands to Manage Welcome Messages:

- /setwelcome <text> : Set a custom welcome message
- /welcome on        : Enable welcome messages
- /welcome off       : Disable welcome messages

Supported Placeholders:
- {username}   : Telegram username
- {first_name} : User's first name
- {mention}    : Mention user in message
- {title}      : Group title

Example:
 /setwelcome Hello {first_name}! Welcome to {title}!
"""
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
        media = InputMediaPhoto(media=START_IMAGE, caption=text)
        await callback_query.message.edit_media(media=media, reply_markup=buttons)
        await callback_query.answer()


    # ==========================================================
    # Locks callback
    # ==========================================================
    @app.on_callback_query(filters.regex("^locks$"))
    async def locks_callback(client, callback_query):
        text = """
╔══════════════════╗
     ⚙ Locks System
╚══════════════════╝

Commands to Manage Locks:

- /lock <type>    : Enable a lock
- /unlock <type>  : Disable a lock
- /locks          : Show active locks
- /lockall        : Lock everything at once 🔐
- /unlockall      : Unlock everything at once 🔓

Available Lock Types:
- url      : Block links/URLs
- sticker  : Block stickers
- media    : Block photos/videos/docs
- username : Block @mention messages
- forward  : Block forwarded messages
- text     : Block ALL text messages
- edit     : Delete edited messages
"""
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
        media = InputMediaPhoto(media=START_IMAGE, caption=text)
        await callback_query.message.edit_media(media=media, reply_markup=buttons)
        await callback_query.answer()


    # ==========================================================
    # Moderation callback
    # ==========================================================
    @app.on_callback_query(filters.regex("^moderation$"))
    async def moderation_callback(client, callback_query):
        try:
            text = """
╔══════════════════╗
      ⚙️ Moderation
╚══════════════════╝

Manage your group easily:

¤ /kick <user>       — Remove a user
¤ /ban <user>        — Ban permanently
¤ /unban <user>      — Lift ban
¤ /mute <user>       — Disable messages
¤ /unmute <user>     — Allow messages again
¤ /tmute <user> <time> — Temp mute (1m–24h)
¤ /tban <user> <time>  — Temp ban (1m–24h)
¤ /warn <user>       — Add warning (3 = mute)
¤ /warns <user>      — View warnings
¤ /resetwarns <user> — Clear all warnings

💡 Usage:
Reply to a user or type /ban @username
"""
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=text)
            await callback_query.message.edit_media(media=media, reply_markup=buttons)
            await callback_query.answer()
        except Exception as e:
            print(f"Error: {e}")
            await callback_query.answer("❌ Something went wrong.", show_alert=True)


    # ==========================================================
    # BioLink callback
    # ==========================================================
    @app.on_callback_query(filters.regex("^biolink$"))
    async def biolink_callback(client, callback_query):
        try:
            text = """
╔══════════════════╗
    🔗 BioLink Protection
╚══════════════════╝

Blocks users who have links in their bio.

Commands:

¤ /biolink on  — Protection ON
¤ /biolink off — Protection OFF

- Bio link detected → message deleted.
- Admins are not affected.
- Bot needs Delete Messages permission.
"""
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=text)
            await callback_query.message.edit_media(media=media, reply_markup=buttons)
            await callback_query.answer()
        except Exception as e:
            print(f"Error: {e}")
            await callback_query.answer("❌ Something went wrong.", show_alert=True)


    # ==========================================================
    # Notes callback
    # ==========================================================
    @app.on_callback_query(filters.regex("^notes_help$"))
    async def notes_help_callback(client, callback_query):
        try:
            text = """
╔════════════════════════╗
   📝 NOTES
╚════════════════════════╝

👮 Admin Commands:
• /setnote <name> <content>
• /delnote <name>

👥 User Commands:
• /notes — List all notes
• #note_name — Get private link
"""
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=text)
            await callback_query.message.edit_media(media=media, reply_markup=buttons)
            await callback_query.answer()
        except Exception as e:
            print(f"Error: {e}")
            await callback_query.answer("❌ Something went wrong.", show_alert=True)


    # ==========================================================
    # Rules callback
    # ==========================================================
    @app.on_callback_query(filters.regex("^rules_help$"))
    async def rules_help_callback(client, callback_query):
        try:
            text = """
╔══════════════════╗
   📜 RULES
╚══════════════════╝

- /setrules <text> — Set group rules
- /rules           — Show current rules
- /clearrules      — Remove all rules

🌟 Formatting is preserved exactly as typed.
"""
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=text)
            await callback_query.message.edit_media(media=media, reply_markup=buttons)
            await callback_query.answer()
        except Exception as e:
            print(f"Error: {e}")
            await callback_query.answer("❌ Something went wrong.", show_alert=True)


    # ==========================================================
    # Abuse callback
    # ==========================================================
    @app.on_callback_query(filters.regex("^abuse_help$"))
    async def abuse_help_callback(client, callback_query):
        try:
            text = """
╔══════════════════╗
   🤬 Abuse Detection
╚══════════════════╝

Abusive messages are automatically deleted.

• /noabuse on  — Enable ✅
• /noabuse off — Disable ❌

- Message deleted instantly.
- 5 second warning sent.
- Admins not affected.
"""
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=text)
            await callback_query.message.edit_media(media=media, reply_markup=buttons)
            await callback_query.answer()
        except Exception as e:
            print(f"Error: {e}")
            await callback_query.answer("❌ Something went wrong.", show_alert=True)


    # ==========================================================
    # FSub callback
    # ==========================================================
    @app.on_callback_query(filters.regex("^fsub_help$"))
    async def fsub_help_callback(client, callback_query):
        try:
            text = """
╔══════════════════╗
   🔗 FORCE-SUBSCRIBE
╚══════════════════╝

Users who haven't joined required
channels cannot send messages.

- /addfsub @channel    — Add channel
- /removefsub @channel — Remove channel
- /fsublist            — List channels

Bot must be admin in the channel.
"""
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=text)
            await callback_query.message.edit_media(media=media, reply_markup=buttons)
            await callback_query.answer()
        except Exception as e:
            print(f"Error: {e}")
            await callback_query.answer("❌ Something went wrong.", show_alert=True)


    # ==========================================================
    # Echo callback
    # ==========================================================
    @app.on_callback_query(filters.regex("^echo_help$"))
    async def echo_help_callback(client, callback_query):
        try:
            from handlers.tools import LONGMSG_HELP_TEXT
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=LONGMSG_HELP_TEXT)
            await callback_query.message.edit_media(media=media, reply_markup=buttons)
            await callback_query.answer()
        except Exception as e:
            print(f"Error: {e}")
            await callback_query.answer("❌ Something went wrong.", show_alert=True)


    # ==========================================================
    # Phone callback
    # ==========================================================
    @app.on_callback_query(filters.regex("^phone_help$"))
    async def phone_help_callback(client, callback_query):
        try:
            from handlers.tools import PHONE_HELP_TEXT
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=PHONE_HELP_TEXT)
            await callback_query.message.edit_media(media=media, reply_markup=buttons)
            await callback_query.answer()
        except Exception as e:
            print(f"Error: {e}")
            await callback_query.answer("❌ Something went wrong.", show_alert=True)


    # ==========================================================
    # Long message callback
    # ==========================================================
    @app.on_callback_query(filters.regex("^longmsg_help$"))
    async def longmsg_help_callback(client, callback_query):
        try:
            from handlers.tools import LONGMSG_HELP_TEXT
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=LONGMSG_HELP_TEXT)
            await callback_query.message.edit_media(media=media, reply_markup=buttons)
            await callback_query.answer()
        except Exception as e:
            print(f"Error: {e}")
            await callback_query.answer("❌ Something went wrong.", show_alert=True)


    # ==========================================================
    # Hashtag callback
    # ==========================================================
    @app.on_callback_query(filters.regex("^hashtag_help$"))
    async def hashtag_help_callback(client, callback_query):
        try:
            from handlers.tools import HASHTAG_HELP_TEXT
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=HASHTAG_HELP_TEXT)
            await callback_query.message.edit_media(media=media, reply_markup=buttons)
            await callback_query.answer()
        except Exception as e:
            print(f"Error: {e}")
            await callback_query.answer("❌ Something went wrong.", show_alert=True)


    # ==========================================================
    # Utility callback
    # ==========================================================
    @app.on_callback_query(filters.regex("^utility_help$"))
    async def utility_help_callback(client, callback_query):
        try:
            from handlers.utility import UTILITY_HELP_TEXT
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=UTILITY_HELP_TEXT)
            await callback_query.message.edit_media(media=media, reply_markup=buttons)
            await callback_query.answer()
        except Exception as e:
            print(f"Error: {e}")
            await callback_query.answer("❌ Something went wrong.", show_alert=True)


    # ==========================================================
    # Cmd deleter callback
    # ==========================================================
    @app.on_callback_query(filters.regex("^cmd_help$"))
    async def cmd_help_callback(client, callback_query):
        try:
            from handlers.cmddeleter import CMDDELETER_HELP_TEXT
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=CMDDELETER_HELP_TEXT)
            await callback_query.message.edit_media(media=media, reply_markup=buttons)
            await callback_query.answer()
        except Exception as e:
            print(f"Error: {e}")
            await callback_query.answer("❌ Something went wrong.", show_alert=True)


    # ==========================================================
    # Media delete callback
    # ==========================================================
    @app.on_callback_query(filters.regex("^mediadelete_help$"))
    async def mediadelete_help_callback(client, callback_query):
        try:
            from handlers.mediadelete import MEDIADELETE_HELP_TEXT
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=MEDIADELETE_HELP_TEXT)
            await callback_query.message.edit_media(media=media, reply_markup=buttons)
            await callback_query.answer()
        except Exception as e:
            print(f"Error: {e}")
            await callback_query.answer("❌ Something went wrong.", show_alert=True)


    # ==========================================================
    # Cleaner callback
    # ==========================================================
    @app.on_callback_query(filters.regex("^cleaner_help$"))
    async def cleaner_help_callback(client, callback_query):
        try:
            from handlers.cleaner import CLEANER_HELP_TEXT
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=CLEANER_HELP_TEXT)
            await callback_query.message.edit_media(media=media, reply_markup=buttons)
            await callback_query.answer()
        except Exception as e:
            print(f"Error: {e}")
            await callback_query.answer("❌ Something went wrong.", show_alert=True)


    # ==========================================================
    # Zombie callback
    # ==========================================================
    @app.on_callback_query(filters.regex("^zombie_help$"))
    async def zombie_help_callback(client, callback_query):
        try:
            from handlers.zombie import ZOMBIE_HELP_TEXT
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=ZOMBIE_HELP_TEXT)
            await callback_query.message.edit_media(media=media, reply_markup=buttons)
            await callback_query.answer()
        except Exception as e:
            print(f"Error: {e}")
            await callback_query.answer("❌ Something went wrong.", show_alert=True)


    # ==========================================================
    # Tag All callback
    # ==========================================================
    @app.on_callback_query(filters.regex("^tagall_help$"))
    async def tagall_help_callback(client, callback_query):
        try:
            from handlers.tagall import TAGALL_HELP_TEXT
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=TAGALL_HELP_TEXT)
            await callback_query.message.edit_media(media=media, reply_markup=buttons)
            await callback_query.answer()
        except Exception as e:
            print(f"Error: {e}")
            await callback_query.answer("❌ Something went wrong.", show_alert=True)


    # ==========================================================
    # Promote callback
    # ==========================================================
    @app.on_callback_query(filters.regex("^promote_help$"))
    async def promote_help_callback(client, callback_query):
        try:
            from handlers.promote import PROMOTE_HELP_TEXT
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=PROMOTE_HELP_TEXT)
            await callback_query.message.edit_media(media=media, reply_markup=buttons)
            await callback_query.answer()
        except Exception as e:
            print(f"Error: {e}")
            await callback_query.answer("❌ Something went wrong.", show_alert=True)


    # ==========================================================
    # Broadcast
    # ==========================================================
    @app.on_message(filters.private & filters.command("broadcast"))
    async def broadcast_message(client, message):
        if not message.reply_to_message:
            return await message.reply_text("⚠️ Please reply to a message to broadcast it.")

        if message.from_user.id != OWNER_ID:
            return await message.reply_text("❌ Only the bot owner can use this command.")

        text_to_send = message.reply_to_message.text or message.reply_to_message.caption
        if not text_to_send:
            return await message.reply_text("⚠️ The replied message has no text.")

        users = await db.get_all_users()
        sent, failed = 0, 0
        await message.reply_text(f"📢 Broadcasting to {len(users)} users...")

        for user_id in users:
            try:
                await client.send_message(user_id, text_to_send)
                sent += 1
            except Exception:
                failed += 1

        await message.reply_text(f"✅ Done!\n\nSent: {sent}\nFailed: {failed}")


    # ==========================================================
    # Stats
    # ==========================================================
    @app.on_message(filters.private & filters.command("stats"))
    async def stats_command(client, message):
        if message.from_user.id != OWNER_ID:
            return await message.reply_text("❌ Only the bot owner can use this command.")

        users = await db.get_all_users()
        return await message.reply_text(f"💡 Total users: {len(users)}")
