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
✨ ʜᴇʏ {ᴜsᴇʀ}! 👋  
ɪ’ᴍ EDITH 🤖 — ʏᴏᴜʀ sᴍᴧʀᴛ ɢʀᴏᴜᴘ ɢᴜᴧʀᴅɪᴧɴ.

ʜɪɢʜʟɪɢʜᴛs:
────────────────────────
• sᴍᴧʀᴛ ᴧɴᴛɪ-sᴘᴧᴍ & ʟɪɴᴋ sʜɪᴇʟᴅ ⚡  
• ᴧᴅᴧᴘᴛɪᴠᴇ ʟᴏᴄᴋ sʏsᴛᴇᴍ 🔒  
• ʙɪᴏʟɪɴᴋ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ 🛡️  
• ɴᴏᴛᴇs & ʀᴜʟᴇs ᴍᴧɴᴧɢᴇᴍᴇɴᴛ 📌  

⚡ ғᴧsᴛ • sᴇᴄᴜʀᴇ • ʀᴇʟɪᴧʙʟᴇ
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
    # /start — Normal start + note deep link handle
    # ==========================================================
    @app.on_message(filters.private & filters.command("start"))
    async def start_command(client, message):
        args = message.text.split(maxsplit=1)

        # Note deep link check: /start note_chatid_notename
        if len(args) > 1 and args[1].startswith("note_"):
            payload = args[1]
            try:
                _, chat_id_str, name = payload.split("_", 2)
                chat_id = int(chat_id_str)
            except (ValueError, IndexError):
                return await message.reply_text("❌ Invalid note link.")

            content = await db.get_note(chat_id, name)
            if not content:
                return await message.reply_text(f"⚠️ Note `#{name}` nahi mila ya delete ho gaya.")

            return await message.reply_text(
                f"╔════════════════════════╗\n"
                f"   📝 Note: #{name}\n"
                f"╚════════════════════════╝\n\n"
                f"{content}"
            )

        # Normal /start
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
  ⚙ 𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗦𝗬𝗦𝗧𝗘𝗠
╚══════════════════╝

🎚️ᴄᴏᴍᴍᴀɴᴅs ᴛᴏ ᴍᴀɴᴀɢᴇ ᴡᴇʟᴄᴏᴍᴇ ᴍᴇssᴀɢᴇs:

¤ /setwelcome : sᴇᴛ ᴀ ᴄᴜsᴛᴏᴍ ᴡᴇʟᴄᴏᴍᴇ ᴍᴇssᴀɢᴇ ғᴏʀ ʏᴏᴜʀ ɢʀᴏᴜᴘ
¤ /welcome on : ᴇɴᴀʙʟᴇ ᴛʜᴇ ᴡᴇʟᴄᴏᴍᴇ ᴍᴇssᴀɢᴇs
¤ /welcome off : ᴅɪsᴀʙʟᴇ ᴛʜᴇ ᴡᴇʟᴄᴏᴍᴇ ᴍᴇssᴀɢᴇs

🎛️ sᴜᴘᴘᴏʀᴛᴇᴅ ᴘʟᴀᴄᴇʜᴏʟᴅᴇʀs:

¤ {ᴜsᴇʀɴᴀᴍᴇ} : ᴛᴇʟᴇɢʀᴀᴍ ᴜsᴇʀɴᴀᴍᴇ
¤ {ғɪʀsᴛ_ɴᴀᴍᴇ} : ᴜsᴇʀ's ғɪʀsᴛ ɴᴀᴍᴇ
¤ {ɪᴅ} : ᴜsᴇʀ ɪᴅ
¤ {ᴍᴇɴᴛɪᴏɴ} : ᴍᴇɴᴛɪᴏɴ ᴜsᴇʀ ɪɴ ᴍᴇssᴀɢᴇ

🧾 ᴇxᴀᴍᴘʟᴇ:
¤ /sᴇᴛᴡᴇʟᴄᴏᴍᴇ ʜᴇʟʟᴏ {ғɪʀsᴛ_ɴᴀᴍᴇ}! ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ {ᴛɪᴛʟᴇ}!
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

Available Lock Types:
- url      : Block links/URLs
- sticker  : Block stickers
- media    : Block photos/videos/docs
- username : Block @mention messages
- forward  : Block forwarded messages
- text     : Block ALL text messages
- edit     : Delete edited messages

Example:
 /lock text   → Koi bhi text msg nahi kar payega
 /lock edit   → Koi edit kare to message delete hoga
 /unlock url  → Links phir allow honge
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
¤ /warn <user>       — Add warning (3 = mute)
¤ /warns <user>      — View warnings
¤ /resetwarns <user> — Clear all warnings
¤ /promote <user>    — Make admin
¤ /demote <user>     — Remove from admin

💡 Usage:
Reply to a user or type /ban @username
"""
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=text)
            await callback_query.message.edit_media(media=media, reply_markup=buttons)
            await callback_query.answer()
        except Exception as e:
            print(f"Error in moderation_callback: {e}")
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

Un users ko rokta hai jinke bio me
koi bhi link hota hai.

Commands:

¤ /biolink on  — Protection ON karo
¤ /biolink off — Protection OFF karo

Kaise kaam karta hai:
- Jab user message karta hai, bot
  uski bio check karta hai.
- Bio me link mila → message delete.
- User ko samjhaya jaata hai.

Note:
- Admins par apply nahi hota.
- Bot ko Delete Messages permission
  chahiye.
"""
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=text)
            await callback_query.message.edit_media(media=media, reply_markup=buttons)
            await callback_query.answer()
        except Exception as e:
            print(f"Error in biolink_callback: {e}")
            await callback_query.answer("❌ Something went wrong.", show_alert=True)


    # ==========================================================
    # Notes help callback
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
  → Note save karo

• /delnote <name>
  → Note delete karo

👥 User Commands:
• /notes
  → Sabke notes ki list dekho
  (Har note ka private link milega)

• #note_name
  → Group me type karo, bot
    private link bhejega

💡 Example:
 /setnote welcome Yahan spam mat karo!
 #welcome  → Note ka link milega
"""
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=text)
            await callback_query.message.edit_media(media=media, reply_markup=buttons)
            await callback_query.answer()
        except Exception as e:
            print(f"Error in notes_help_callback: {e}")
            await callback_query.answer("❌ Something went wrong.", show_alert=True)


    # ==========================================================
    # Rules help callback
    # ==========================================================
    @app.on_callback_query(filters.regex("^rules_help$"))
    async def rules_help_callback(client, callback_query):
        try:
            text = """
╔══════════════════╗
   📜 RULES
╚══════════════════╝

🛠️ Commands:

- /setrules <text>
  → Group rules set karo

- /rules
  → Current rules dikhao

- /clearrules
  → Sabke rules hatao

🌟 Note:
Jaise bhi likhoge — spaces, newlines,
formatting — waisa hi save hoga.
Kuch bhi auto-change nahi hoga.

Example:
 /setrules
 1. Spam mat karo
 2. Respect karo sabko
 3. Links share mat karo
"""
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=text)
            await callback_query.message.edit_media(media=media, reply_markup=buttons)
            await callback_query.answer()
        except Exception as e:
            print(f"Error in rules_help_callback: {e}")
            await callback_query.answer("❌ Something went wrong.", show_alert=True)



    # ==========================================================
    # Abuse help callback
    # ==========================================================
    @app.on_callback_query(filters.regex("^abuse_help$"))
    async def abuse_help_callback(client, callback_query):
        try:
            text = """
╔══════════════════╗
   🤬 Abuse Detection
╚══════════════════╝

Gaaliyan dene walo ka message
automatically delete ho jaata hai.

🔧 Commands:

• /noabuse on  — Detection ON karo ✅
• /noabuse off — Detection OFF karo ❌

Kaise kaam karta hai:
- Koi bhi abusive word type kare,
  message turant delete hoga.
- User ko 5 second ki warning
  message milti hai.

Note:
- Admins par apply nahi hota.
- Bot ko Delete Messages permission
  chahiye.
"""
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=text)
            await callback_query.message.edit_media(media=media, reply_markup=buttons)
            await callback_query.answer()
        except Exception as e:
            print(f"Error in abuse_help_callback: {e}")
            await callback_query.answer("❌ Something went wrong.", show_alert=True)


    # ==========================================================
    # FSub help callback
    # ==========================================================
    @app.on_callback_query(filters.regex("^fsub_help$"))
    async def fsub_help_callback(client, callback_query):
        try:
            text = """
╔══════════════════╗
   🔗 FORCE-SUBSCRIBE
╚══════════════════╝

Jo users required channels join
nahi karte, unka message delete
hota hai aur join links milte hain.

📢 Commands:

- /addfsub <channel>
  → Channel add karo

- /removefsub <channel>
  → Channel remove karo

- /fsublist
  → Sabke channels ki list

Note:
- Bot ko channel ka admin banana
  padega pehle.
- 30 second baad warn message
  auto-delete ho jaata hai.

Example:
 /addfsub @MyChannel
 /removefsub @MyChannel
"""
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=text)
            await callback_query.message.edit_media(media=media, reply_markup=buttons)
            await callback_query.answer()
        except Exception as e:
            print(f"Error in fsub_help_callback: {e}")
            await callback_query.answer("❌ Something went wrong.", show_alert=True)


    # ==========================================================
    # Broadcast Command
    # ==========================================================
    @app.on_message(filters.private & filters.command("broadcast"))
    async def broadcast_message(client, message):
        if not message.reply_to_message:
            return await message.reply_text("⚠️ Please reply to a message to broadcast it.")

        if message.from_user.id != OWNER_ID:
            return await message.reply_text("❌ Only the bot owner can use this command.")

        text_to_send = message.reply_to_message.text or message.reply_to_message.caption
        if not text_to_send:
            return await message.reply_text("⚠️ The replied message has no text to send.")

        users = await db.get_all_users()
        sent, failed = 0, 0

        await message.reply_text(f"📢 Broadcasting to {len(users)} users...")

        for user_id in users:
            try:
                await client.send_message(user_id, text_to_send)
                sent += 1
            except Exception:
                failed += 1

        await message.reply_text(f"✅ Broadcast finished!\n\nSent: {sent}\nFailed: {failed}")


    # ==========================================================
    # Stats Command
    # ==========================================================
    @app.on_message(filters.private & filters.command("stats"))
    async def stats_command(client, message):
        if message.from_user.id != OWNER_ID:
            return await message.reply_text("❌ Only the bot owner can use this command.")

        users = await db.get_all_users()
        return await message.reply_text(f"💡 Total users: {len(users)}")
