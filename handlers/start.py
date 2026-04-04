# ============================================================
# Group Manager Bot
# Author: Mr. Stark
# ============================================================

from pyrogram import Client, filters, enums
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
        text = (
            f"✨ <b>ʜᴇʏ {user}! 👋</b> ✨\n\n"
            f"<b>❍ ɪ’ᴍ EDITH 🤖 — ʏᴏᴜʀ sᴍᴧʀᴛ ɢʀᴏᴜᴘ ɢᴜᴧʀᴅɪᴧɴ.</b>\n\n"
            f"<b>❖ ʜɪɢʜʟɪɢʜᴛs ❖</b>\n"
            f"<b>◈ ━━━ ✦ ━━━ ❖ ━━━ ✦ ━━━ ◈</b>\n"
            f"<b>➻ sᴍᴧʀᴛ ᴧɴᴛɪ-sᴘᴧᴍ & ʟɪɴᴋ sʜɪᴇʟᴅ ⚡</b>\n"
            f"<b>➻ ᴧᴅᴧᴘᴛɪᴠᴇ ʟᴏᴄᴋ sʏsᴛᴇᴍ 🔒</b>\n"
            f"<b>➻ ʙɪᴏʟɪɴᴋ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ 🛡️</b>\n"
            f"<b>➻ ɴᴏᴛᴇs & ʀᴜʟᴇs ᴍᴧɴᴧɢᴇᴍᴇɴᴛ 📌</b>\n\n"
            f"<b>✦ ғᴧsᴛ ✦ sᴇᴄᴜʀᴇ ✦ ʀᴇʟɪᴧʙʟᴇ ✦</b>"
        )


        
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
            await message.reply_photo(START_IMAGE, caption=text, reply_markup=buttons, parse_mode=enums.ParseMode.HTML)
        else:
            media = InputMediaPhoto(media=START_IMAGE, caption=text, parse_mode=enums.ParseMode.HTML)
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
                return await message.reply_text("❌ <b>Invalid note link.</b>", parse_mode=enums.ParseMode.HTML)

            content = await db.get_note(chat_id, name)
            if not content:
                return await message.reply_text(
                    f"⚠️ Note <b>#{name}</b> nahi mila ya delete ho gaya.",
                    parse_mode=enums.ParseMode.HTML
                )

            return await message.reply_text(
                f"╔════════════════════════╗\n"
                f"   📝 <b>Note: #{name}</b>\n"
                f"╚════════════════════════╝\n\n"
                f"{content}",
                parse_mode=enums.ParseMode.HTML
            )

        # Normal /start
        user = message.from_user
        await db.add_user(user.id, user.first_name)
        await send_start_menu(message, user.first_name)


    # ==========================================================
    # Help Menu helper
    # ==========================================================
    async def send_help_menu(message):
        text = (
            "╔══════════════════╗\n"
            "     <b>Help Menu</b>\n"
            "╚══════════════════╝\n\n"
            "Choose a category below to explore commands:\n"
            "─────────────────────────────\n"
        )
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

        media = InputMediaPhoto(media=START_IMAGE, caption=text, parse_mode=enums.ParseMode.HTML)
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
        text = (
            f"<b>╔══════════════════╗</b>\n"
            f"<b>   ⚙ ᴡᴇʟᴄᴏᴍᴇ sʏsᴛᴇᴍ</b>\n"
            f"<b>╚══════════════════╝</b>\n\n"
            f"<b>❖ ᴄᴏᴍᴍᴀɴᴅs ᴛᴏ ᴍᴀɴᴀɢᴇ ᴡᴇʟᴄᴏᴍᴇ ᴍᴇssᴀɢᴇs:</b>\n\n"
            f"➻ /setwelcome &lt;text&gt; : <b>sᴇᴛ ᴀ ᴄᴜsᴛᴏᴍ ᴡᴇʟᴄᴏᴍᴇ ᴍᴇssᴀɢᴇ</b>\n"
            f"➻ /welcome on        : <b>ᴇɴᴀʙʟᴇ ᴡᴇʟᴄᴏᴍᴇ ᴍᴇssᴀɢᴇs</b>\n"
            f"➻ /welcome off       : <b>ᴅɪsᴀʙʟᴇ ᴡᴇʟᴄᴏᴍᴇ ᴍᴇssᴀɢᴇs</b>\n\n"
            f"<b>❖ sᴜᴘᴘᴏʀᴛᴇᴅ ᴘʟᴀᴄᴇʜᴏʟᴅᴇʀs ❖</b>\n"
            f"<b>➻ <code>{'{'}username{'}'}</code>   : ᴛᴇʟᴇɢʀᴀᴍ ᴜsᴇʀɴᴀᴍᴇ</b>\n"
            f"<b>➻ <code>{'{'}first_name{'}'}</code> : ᴜsᴇʀ's ғɪʀsᴛ ɴᴀᴍᴇ</b>\n"
            f"<b>➻ <code>{'{'}mention{'}'}</code>    : ᴍᴇɴᴛɪᴏɴ ᴜsᴇʀ ɪɴ ᴍᴇssᴀɢᴇ</b>\n"
            f"<b>➻ <code>{'{'}title{'}'}</code>      : ɢʀᴏᴜᴘ ᴛɪᴛʟᴇ</b>\n\n"
            f"<b>❖ ᴇxᴀᴍᴘʟᴇ ❖</b>\n"
            f"❍ /setwelcome Hello {'{'}first_name{'}'}! Welcome to {'{'}title{'}'}!\n"
        )

        
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
        media = InputMediaPhoto(media=START_IMAGE, caption=text, parse_mode=enums.ParseMode.HTML)
        await callback_query.message.edit_media(media=media, reply_markup=buttons)
        await callback_query.answer()


    # ==========================================================
    # Locks callback
    # ==========================================================
    @app.on_callback_query(filters.regex("^locks$"))
    async def locks_callback(client, callback_query):
        text = (
            f"<b>╔══════════════════╗</b>\n"
            f"<b>    ⚙ ʟᴏᴄᴋs sʏsᴛᴇᴍ</b>\n"
            f"<b>╚══════════════════╝</b>\n\n"
            f"<b>❖ ᴄᴏᴍᴍᴀɴᴅs ᴛᴏ ᴍᴀɴᴀɢᴇ ʟᴏᴄᴋs ❖</b>\n\n"
            f"➻ /lock <type> : <b>ᴇɴᴀʙʟᴇ ᴀ ʟᴏᴄᴋ</b>\n"
            f"➻ /unlock <type> : <b>ᴅɪsᴀʙʟᴇ ᴀ ʟᴏᴄᴋ</b>\n"
            f"➻ /locks : <b>sʜᴏᴡ ᴀᴄᴛɪᴠᴇ ʟᴏᴄᴋs</b>\n\n"
            f"<b>❖ ᴀᴠᴀɪʟᴀʙʟᴇ ʟᴏᴄᴋ ᴛʏᴘᴇs ❖</b>\n"
            f"<b>➻ <code>url</code>      : ʙʟᴏᴄᴋ ʟɪɴᴋs/ᴜʀʟs</b>\n"
            f"<b>➻ <code>sticker</code>  : ʙʟᴏᴄᴋ sᴛɪᴄᴋᴇʀs</b>\n"
            f"<b>➻ <code>media</code>    : ʙʟᴏᴄᴋ ᴘʜᴏᴛᴏs/ᴠɪᴅᴇᴏs/ᴅᴏᴄs</b>\n"
            f"<b>➻ <code>username</code> : ʙʟᴏᴄᴋ @ᴍᴇɴᴛɪᴏɴ ᴍᴇssᴀɢᴇs</b>\n"
            f"<b>➻ <code>forward</code>  : ʙʟᴏᴄᴋ ғᴏʀᴡᴀʀᴅᴇᴅ ᴍᴇssᴀɢᴇs</b>\n"
            f"<b>➻ <code>text</code>     : ʙʟᴏᴄᴋ ᴀʟʟ ᴛᴇxᴛ ᴍᴇssᴀɢᴇs</b>\n"
            f"<b>➻ <code>edit</code>     : ᴅᴇʟᴇᴛᴇ ᴇᴅɪᴛᴇᴅ ᴍᴇssᴀɢᴇs</b>\n\n"
            f"<b>❖ ᴇxᴀᴍᴘʟᴇ ❖</b>\n"
            f"❍ /lock text ➻ <b>ᴋᴏɪ ʙʜɪ ᴛᴇxᴛ ᴍsɢ ɴᴀʜɪ ᴋᴀʀ ᴘᴀʏᴇɢᴀ</b>\n"
            f"❍ /lock edit ➻ <b>ᴋᴏɪ ᴇᴅɪᴛ ᴋᴀʀᴇ ᴛᴏ ᴍᴇssᴀɢᴇ ᴅᴇʟᴇᴛᴇ ʜᴏɢᴀ</b>\n"
            f"❍ /unlock url ➻ <b>ʟɪɴᴋs ᴘʜɪʀ ᴀʟʟᴏᴡ ʜᴏɴɢᴇ</b>\n"
        )

        
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
        media = InputMediaPhoto(media=START_IMAGE, caption=text, parse_mode=enums.ParseMode.HTML)
        await callback_query.message.edit_media(media=media, reply_markup=buttons)
        await callback_query.answer()


    # ==========================================================
    # Moderation callback
    # ==========================================================
    @app.on_callback_query(filters.regex("^moderation$"))
    async def moderation_callback(client, callback_query):
        try:
            text = (
                f"<b>╔══════════════════╗</b>\n"
                f"<b>    ⚙️ ᴍᴏᴅᴇʀᴀᴛɪᴏɴ</b>\n"
                f"<b>╚══════════════════╝</b>\n\n"
                f"<b>❖ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴇᴀsɪʟʏ ❖</b>\n\n"
                f"➻ /kick <user>  — <b>ʀᴇᴍᴏᴠᴇ ᴀ ᴜsᴇʀ</b>\n"
                f"➻ /ban <user>   — <b>ʙᴀɴ ᴘᴇʀᴍᴀɴᴇɴᴛʟʏ</b>\n"
                f"➻ /unban <user>  — <b>ʟɪғᴛ ʙᴀɴ</b>\n"
                f"➻ /mute <user>  — <b>ᴅɪsᴀʙʟᴇ ᴍᴇssᴀɢᴇs</b>\n"
                f"➻ /unmute <user>  — <b>ᴀʟʟᴏᴡ ᴍᴇssᴀɢᴇs ᴀɢᴀɪɴ</b>\n"
                f"➻ /warn <user>  — <b>ᴀᴅᴅ ᴡᴀʀɴɪɴɢ (3 = ᴍᴜᴛᴇ)</b>\n"
                f"➻ /warns <user>  — <b>ᴠɪᴇᴡ ᴡᴀʀɴɪɴɢs</b>\n"
                f"➻ /resetwarns <user> — <b>ᴄʟᴇᴀʀ ᴀʟʟ ᴡᴀʀɴɪɴɢs</b>\n"
                f"➻ /promote <user>  — <b>ᴍᴀᴋᴇ ᴀᴅᴍɪɴ</b>\n"
                f"➻ /demote <user>  — <b>ʀᴇᴍᴏᴠᴇ ғʀᴏᴍ ᴀᴅᴍɪɴ</b>\n\n"
                f"<b>❖💡 ᴜsᴀɢᴇ ❖</b>\n"
                f"❍ <b>ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ ᴏʀ ᴛʏᴘᴇ /ban @username</b>\n"
            )
            
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=text, parse_mode=enums.ParseMode.HTML)
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
            text = (
                f"<b>╔══════════════════╗</b>\n"
                f"<b>    🔗 ʙɪᴏʟɪɴᴋ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ</b>\n"
                f"<b>╚══════════════════╝</b>\n\n"
                f"<b>❖ ᴘʀᴇᴠᴇɴᴛs ᴜsᴇʀs ᴡɪᴛʜ ʟɪɴᴋs ɪɴ ᴛʜᴇɪʀ ʙɪᴏ ғʀᴏᴍ sᴇɴᴅɪɴɢ ᴍᴇssᴀɢᴇs.</b>\n\n"
                f"<b>❍ ᴄᴏᴍᴍᴀɴᴅs ❍</b>\n\n"
                f"➻ /biolink on  — <b>ᴇɴᴀʙʟᴇ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ</b>\n"
                f"➻ /biolink off — <b>ᴅɪsᴀʙʟᴇ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ</b>\n\n"
                f"<b>❖ ʜᴏᴡ ɪᴛ ᴡᴏʀᴋs ❖</b>\n"
                f"<b>➻ ᴡʜᴇɴ ᴀ ᴜsᴇʀ sᴇɴᴅs ᴀ ᴍᴇssᴀɢᴇ, ᴛʜᴇ ʙᴏᴛ ᴄʜᴇᴄᴋs ᴛʜᴇɪʀ ʙɪᴏ.</b>\n"
                f"<b>➻ ɪғ ᴀ ʟɪɴᴋ ɪs ғᴏᴜɴᴅ → ᴛʜᴇ ᴍᴇssᴀɢᴇ ɪs ᴅᴇʟᴇᴛᴇᴅ.</b>\n"
                f"<b>➻ ᴛʜᴇ ᴜsᴇʀ ɪs ɴᴏᴛɪғɪᴇᴅ ᴀᴄᴄᴏʀᴅɪɴɢʟʏ.</b>\n\n"
                f"<b>❖ ɴᴏᴛᴇ ❖</b>\n"
                f"<b>➻ ᴀᴅᴍɪɴs ᴀʀᴇ ᴇxᴇᴍᴘᴛᴇᴅ ғʀᴏᴍ ᴛʜɪs ʀᴜʟᴇ.</b>\n"
                f"<b>➻ ᴛʜᴇ ʙᴏᴛ ᴍᴜsᴛ ʜᴀᴠᴇ 'ᴅᴇʟᴇᴛᴇ ᴍᴇssᴀɢᴇs' ᴘᴇʀᴍɪssɪᴏɴ.</b>\n"
           )
            
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=text, parse_mode=enums.ParseMode.HTML)
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
            text = (
                f"<b>╔════════════════════════╗</b>\n"
                f"<b>   📝 ɴᴏᴛᴇs</b>\n"
                f"<b>╚════════════════════════╝</b>\n\n"
                f"<b>👮 ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs:</b>\n"
                f"❍ /setnote <name> <content> ➻ <b> sᴀᴠᴇ ᴀ ɴᴏᴛᴇ</b>\n"
                f"❍ /delnote <name> ➻ <b> ᴅᴇʟᴇᴛᴇ ᴀ ɴᴏᴛᴇ</b>\n\n"
                f"<b>👥 ᴜsᴇʀ ᴄᴏᴍᴍᴀɴᴅs</b>\n"
                f"❍ /notes ➻ <b>ᴠɪᴇᴡ ᴀʟʟ sᴀᴠᴇᴅ ɴᴏᴛᴇs. (ᴇᴀᴄʜ ɴᴏᴛᴇ ɪɴᴄʟᴜᴅᴇs ᴀ ᴘʀɪᴠᴀᴛᴇ ʟɪɴᴋ)</b>\n\n"
                f"❍ #note_name <b>➻ ғᴏʀ sᴇᴇ ɴᴏᴛᴇs. (ᴛʜᴇ ɴᴏᴛᴇ ᴠɪᴀ ᴘʀɪᴠᴀᴛᴇ ʟɪɴᴋ)</b>\n\n"
                f"<b>💡 ᴇxᴀᴍᴘʟᴇ:</b>\n"
                f"➻ /setnote welcome Don't spam here!\n"
                f"❍ #welcome ➻ <b>ᴛʜᴇɴ ʏᴏᴜ ɢᴇᴛ ᴀ ʟɪɴᴋ ᴏғ ᴛʜɪs ɴᴏᴛᴇ</b>\n"
            )
            
            
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=text, parse_mode=enums.ParseMode.HTML)
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
            text = (
                "╔══════════════════╗\n"
                "   📜 <b>RULES</b>\n"
                "╚══════════════════╝\n\n"
                "🛠️ <b>Commands:</b>\n\n"
                "- <b>/setrules</b> &lt;text&gt;\n"
                "  → Group rules set karo\n\n"
                "- <b>/rules</b>\n"
                "  → Current rules dikhao\n\n"
                "- <b>/clearrules</b>\n"
                "  → Sabke rules hatao\n\n"
                "🌟 <b>Note:</b>\n"
                "Jaise bhi likhoge — spaces, newlines,\n"
                "formatting — waisa hi save hoga.\n"
                "Kuch bhi auto-change nahi hoga.\n\n"
                "<b>Example:</b>\n"
                " /setrules\n"
                " 1. Spam mat karo\n"
                " 2. Respect karo sabko\n"
                " 3. Links share mat karo\n"
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=text, parse_mode=enums.ParseMode.HTML)
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
            text = (
                "╔══════════════════╗\n"
                "   🤬 <b>Abuse Detection</b>\n"
                "╚══════════════════╝\n\n"
                "Gaaliyan dene walo ka message\n"
                "automatically delete ho jaata hai.\n\n"
                "🔧 <b>Commands:</b>\n\n"
                "• <b>/noabuse on</b>  — Detection ON karo ✅\n"
                "• <b>/noabuse off</b> — Detection OFF karo ❌\n\n"
                "<b>Kaise kaam karta hai:</b>\n"
                "- Koi bhi abusive word type kare,\n"
                "  message turant delete hoga.\n"
                "- User ko 5 second ki warning\n"
                "  message milti hai.\n\n"
                "<b>Note:</b>\n"
                "- Admins par apply nahi hota.\n"
                "- Bot ko Delete Messages permission\n"
                "  chahiye.\n"
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=text, parse_mode=enums.ParseMode.HTML)
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
            text = (
                "╔══════════════════╗\n"
                "   🔗 <b>FORCE-SUBSCRIBE</b>\n"
                "╚══════════════════╝\n\n"
                "Jo users required channels join\n"
                "nahi karte, unka message delete\n"
                "hota hai aur join links milte hain.\n\n"
                "📢 <b>Commands:</b>\n\n"
                "- <b>/addfsub</b> &lt;channel&gt;\n"
                "  → Channel add karo\n\n"
                "- <b>/removefsub</b> &lt;channel&gt;\n"
                "  → Channel remove karo\n\n"
                "- <b>/fsublist</b>\n"
                "  → Sabke channels ki list\n\n"
                "<b>Note:</b>\n"
                "- Bot ko channel ka admin banana\n"
                "  padega pehle.\n"
                "- 30 second baad warn message\n"
                "  auto-delete ho jaata hai.\n\n"
                "<b>Example:</b>\n"
                " /addfsub @MyChannel\n"
                " /removefsub @MyChannel\n"
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=text, parse_mode=enums.ParseMode.HTML)
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
            return await message.reply_text("⚠️ <b>Please reply to a message to broadcast it.</b>", parse_mode=enums.ParseMode.HTML)

        if message.from_user.id != OWNER_ID:
            return await message.reply_text("❌ <b>Only the bot owner can use this command.</b>", parse_mode=enums.ParseMode.HTML)

        text_to_send = message.reply_to_message.text or message.reply_to_message.caption
        if not text_to_send:
            return await message.reply_text("⚠️ <b>The replied message has no text to send.</b>", parse_mode=enums.ParseMode.HTML)

        users = await db.get_all_users()
        sent, failed = 0, 0

        await message.reply_text(f"📢 <b>Broadcasting to {len(users)} users...</b>", parse_mode=enums.ParseMode.HTML)

        for user_id in users:
            try:
                await client.send_message(user_id, text_to_send)
                sent += 1
            except Exception:
                failed += 1

        await message.reply_text(
            f"✅ <b>Broadcast finished!</b>\n\n<b>Sent:</b> {sent}\n<b>Failed:</b> {failed}",
            parse_mode=enums.ParseMode.HTML
        )


    # ==========================================================
    # Stats Command
    # ==========================================================
    @app.on_message(filters.private & filters.command("stats"))
    async def stats_command(client, message):
        if message.from_user.id != OWNER_ID:
            return await message.reply_text("❌ <b>Only the bot owner can use this command.</b>", parse_mode=enums.ParseMode.HTML)

        users = await db.get_all_users()
        return await message.reply_text(
            f"💡 <b>Total users:</b> {len(users)}",
            parse_mode=enums.ParseMode.HTML
        )
