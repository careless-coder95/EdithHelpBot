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
            f"<b><blockquote expandable>\n"
            f"✨ <b>ʜᴇʏ {user} 🤍</b> ✨\n"
            f"<b>❍ ɪ’ᴍ ᴇᴅɪᴛʜ 🤖 — ʏᴏᴜʀ sᴍᴧʀᴛ ɢʀᴏᴜᴘ ɢᴜᴧʀᴅɪᴧɴ.</b>\n"
            f"</blockquote></b>"
            f"<b><blockquote expandable>"
            f"❖ 𝐇𝐈𝐆𝐇𝐋𝐈𝐆𝐇𝐓𝐒 ❖\n"
            f"➻ sᴍᴧʀᴛ ᴧɴᴛɪ-sᴘᴧᴍ & ʟɪɴᴋ sʜɪᴇʟᴅ\n"
            f"➻ ᴧᴅᴧᴘᴛɪᴠᴇ ʟᴏᴄᴋ sʏsᴛᴇᴍ 🔒\n"
            f"➻ ʙɪᴏʟɪɴᴋ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ 🛡️\n"
            f"➻ ɴᴏᴛᴇs & ʀᴜʟᴇs ᴍᴧɴᴧɢᴇᴍᴇɴᴛ 📌\n"
            f"✦ ғᴧsᴛ ✦ sᴇᴄᴜʀᴇ ✦ ʀᴇʟɪᴧʙʟᴇ ✦\n"
            f"</blockquote></b>"
        )


        
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("✙ 𝐀ᴅᴅ 𝐌є 𝐈η 𝐘συʀ 𝐆ʀσυᴘ ✙", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
            [InlineKeyboardButton("⌯ 𝐇ᴇʟᴘ 𝐀ɴᴅ 𝐂ᴏᴍᴍᴀɴᴅs ⌯", callback_data="help")],
            [
                InlineKeyboardButton(" ⌯ 𝐒ᴜᴘᴘᴏʀᴛ ⌯", url=SUPPORT_GROUP),
                InlineKeyboardButton("⌯ 𝐔ᴘᴅᴀᴛᴇ ⌯", url=UPDATE_CHANNEL),
            ],
           [InlineKeyboardButton("⌯ 𝐌ʏ 𝐌ᴧsᴛᴇʀ ⌯", url=f"https://t.me/CarelessxOwner")]
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
                f"╔═════════════════════╗\n"
                f"   📝 <b>Note: #{name}</b>\n"
                f"╚═════════════════════╝\n\n"
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
            f"<b>❍ ᴄʜᴏᴏsᴇ ᴛʜᴇ ᴄᴀᴛᴇɢᴏʀʏ ғᴏʀ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴɴᴀ ɢᴇᴛ ʜᴇʟᴘ.</b>\n"
            f"<b>❍ ғᴏʀ ᴀɴʏ ǫᴜᴇʀɪᴇs, ᴀsᴋ ɪɴ <a href='https://t.me/CarelessxWorld'>sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ</a>.</b>\n\n"
            f"<b>❍ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ: /</b>"
        )
        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("• 𝐆ʀᴇᴇᴛɪɴɢs •", callback_data="greetings"),
                InlineKeyboardButton("• 𝐌ᴏᴅᴇʀᴀᴛɪᴏɴ •", callback_data="moderation"),
            ],
            [
                InlineKeyboardButton("• 𝐋ᴏᴄᴋs •", callback_data="locks"),
                InlineKeyboardButton("• 𝐁ɪᴏ 𝐋ɪɴᴋ •", callback_data="biolink"),
                InlineKeyboardButton("• 𝐔ᴛɪʟɪᴛʏ •", callback_data="utility_help"),
            ],
            [
                InlineKeyboardButton("• 𝐍ᴏᴛᴇs •", callback_data="notes_help"),
                InlineKeyboardButton("• 𝐑ᴜʟᴇs •", callback_data="rules_help"),
                InlineKeyboardButton("• 𝐀ʙᴜsᴇ •", callback_data="abuse_help"),
            ],
            [
                InlineKeyboardButton("• 𝐅-𝐒ᴜʙ •", callback_data="fsub_help"),
                InlineKeyboardButton("• 𝐄ᴄʜᴏ •", callback_data="echo_help"),
                InlineKeyboardButton("• 𝐏ʜᴏɴᴇ •", callback_data="phone_help"),
            ],
            [
                InlineKeyboardButton("• 𝐓ᴀɢ𝐀ʟʟ •", callback_data="tagall_help"),
                InlineKeyboardButton("• 𝐃ᴇʟ 𝐀ᴄᴄ •", callback_data="zombie_help"),
            ],
            [
                InlineKeyboardButton("• 𝐋ᴏɴɢ 𝐋ɪᴍɪᴛ •", callback_data="longmsg_help"),
                InlineKeyboardButton("• #𝐇ᴀ𝐬ʜᴛᴀɢ •", callback_data="hashtag_help"),
            ],
            [
                InlineKeyboardButton("• 𝐌ᴇᴅɪᴀ 𝐂ʟᴇᴀɴᴇʀ •", callback_data="mediadelete_help"),
                InlineKeyboardButton("• 𝐂ᴍᴅ 𝐃ᴇʟᴇᴛᴇʀ •", callback_data="cmd_help"),
                
            ],
                [InlineKeyboardButton("⌯ 𝐁ᴀᴄᴋ ⌯", callback_data="back_to_start")]
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

        
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("⌯ 𝐁ᴀᴄᴋ ⌯", callback_data="help")]])
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
            f"➻ /lockall : <b>ᴇɴᴀʙʟᴇ ᴀʟʟ ʟᴏᴄᴋs</b>\n"
            f"➻ /unlockall : <b>ᴅɪsᴀʙʟᴇ ᴀʟʟ ʟᴏᴄᴋs</b>\n"
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

        
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("⌯ 𝐁ᴀᴄᴋ ⌯", callback_data="help")]])
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
                f"➻ /tban <time>   — <b>ʙᴀɴ ғᴏʀ sᴘᴇᴄɪғɪᴄ ᴛɪᴍᴇ</b>\n"
                f"➻ /unban <user>  — <b>ʟɪғᴛ ʙᴀɴ</b>\n"
                f"➻ /mute <user>  — <b>ᴅɪsᴀʙʟᴇ ᴍᴇssᴀɢᴇs</b>\n"
                f"➻ /mute <time>  — <b>ᴅɪsᴀʙʟᴇ ᴍᴇssᴀɢᴇs ғᴏʀ sᴘᴇᴄɪғɪᴄ ᴛɪᴍᴇ</b>\n"
                f"➻ /unmute <user>  — <b>ᴀʟʟᴏᴡ ᴍᴇssᴀɢᴇs ᴀɢᴀɪɴ</b>\n"
                f"➻ /warn <user>  — <b>ᴀᴅᴅ ᴡᴀʀɴɪɴɢ (3 = ᴍᴜᴛᴇ)</b>\n"
                f"➻ /warns <user>  — <b>ᴠɪᴇᴡ ᴡᴀʀɴɪɴɢs</b>\n"
                f"➻ /resetwarns <user> — <b>ᴄʟᴇᴀʀ ᴀʟʟ ᴡᴀʀɴɪɴɢs</b>\n"
                f"<b>❖💡 ᴜsᴀɢᴇ ❖</b>\n"
                f"❍ <b>ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ ᴏʀ ᴛʏᴘᴇ /ban @username</b>\n"
            )
            
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("⌯ 𝐁ᴀᴄᴋ ⌯", callback_data="help")]])
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
            
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("⌯ 𝐁ᴀᴄᴋ ⌯", callback_data="help")]])
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
                f"<b>╔════════════════════╗</b>\n"
                f"<b>   📝 ɴᴏᴛᴇs</b>\n"
                f"<b>╚════════════════════╝</b>\n\n"
                f"<b>👮 ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs:</b>\n"
                f"❍ /setnote <name> <content> ➻ <b> sᴀᴠᴇ ᴀ ɴᴏᴛᴇ</b>\n"
                f"❍ /delnote <name> ➻ <b> ᴅᴇʟᴇᴛᴇ ᴀ ɴᴏᴛᴇ</b>\n\n"
                f"<b>👥 ᴜsᴇʀ ᴄᴏᴍᴍᴀɴᴅs</b>\n"
                f"❍ /notes ➻ <b>ᴠɪᴇᴡ ᴀʟʟ sᴀᴠᴇᴅ ɴᴏᴛᴇs. (ᴇᴀᴄʜ ɴᴏᴛᴇ ɪɴᴄʟᴜᴅᴇs ᴀ ᴘʀɪᴠᴀᴛᴇ ʟɪɴᴋ)</b>\n\n"
                f"❍ #note_name <b>➻ ғᴏʀ sᴇᴇ ɴᴏᴛᴇs. (ᴛʜᴇ ɴᴏᴛᴇ ᴠɪᴀ ᴘʀɪᴠᴀᴛᴇ ʟɪɴᴋ)</b>\n\n"
                f"<b>💡 ᴇxᴀᴍᴘʟᴇ:</b>\n"
                f"➻ /setnote welcome Don't spam here!\n"
                f"➻ #welcome ➻ <b>ᴛʜᴇɴ ʏᴏᴜ ɢᴇᴛ ᴀ ʟɪɴᴋ ᴏғ ᴛʜɪs ɴᴏᴛᴇ</b>\n"
            )
            
            
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("⌯ 𝐁ᴀᴄᴋ ⌯", callback_data="help")]])
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
                f"<b>╔══════════════════╗</b>\n"
                f"<b>        📜 ʀᴜʟᴇs</b>\n"
                f"<b>╚══════════════════╝</b>\n\n"
                f"<b>🛠️ ᴄᴏᴍᴍᴀɴᴅs:</b>\n\n"
                f"➻ /setrules <text> <b>➻ sᴇᴛ ɢʀᴏᴜᴘ ʀᴜʟᴇs</b>\n\n"
                f"➻ /rules <b>➻ ᴠɪᴇᴡ ᴄᴜʀʀᴇɴᴛ ʀᴜʟᴇs</b>\n\n"
                f"➻ /clearrules <b>➻ ʀᴇᴍᴏᴠᴇ ᴀʟʟ ʀᴜʟᴇs</b>\n\n"
                f"<b>🌟 ɴᴏᴛᴇ:</b>\n"
                f"<b>❍ ʏᴏᴜʀ ᴛᴇxᴛ ɪs sᴀᴠᴇᴅ ᴇxᴀᴄᴛʟʏ ᴀs ʏᴏᴜ ᴡʀɪᴛᴇ ɪᴛ.</b>\n"
                f"<b>❍ sᴘᴀᴄᴇs, ɴᴇᴡʟɪɴᴇs, ᴀɴᴅ ғᴏʀᴍᴀᴛᴛɪɴɢ ᴀʀᴇ ᴘʀᴇsᴇʀᴠᴇᴅ.</b>\n"
                f"<b>❍ ɴᴏ ᴀᴜᴛᴏᴍᴀᴛɪᴄ ᴄʜᴀɴɢᴇs ᴀʀᴇ ᴍᴀᴅᴇ.</b>\n\n"
                f"<b>❖ ᴇxᴀᴍᴘʟᴇ:</b>\n"
                f"➻ /setrules\n"
                f"<b>1. ᴅᴏ ɴᴏᴛ sᴘᴀᴍ</b>\n"
                f"<b>2. ʀᴇsᴘᴇᴄᴛ ᴇᴠᴇʀʏᴏɴᴇ</b>\n"
                f"<b>3. ᴅᴏ ɴᴏᴛ sʜᴀʀᴇ ʟɪɴᴋs</b>\n"
            )
            
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("⌯ 𝐁ᴀᴄᴋ ⌯", callback_data="help")]])
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
                f"<b>╔══════════════════╗</b>\n"
                f"<b>    ᴀʙᴜsᴇ ᴅᴇᴛᴇᴄᴛɪᴏɴ</b>\n"
                f"<b>╚══════════════════╝</b>\n\n"
                f"<b>❖ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴅᴇʟᴇᴛᴇs ᴍᴇssᴀɢᴇs ᴄᴏɴᴛᴀɪɴɪɴɢ ᴀʙᴜsɪᴠᴇ ʟᴀɴɢᴜᴀɢᴇ.</b>\n\n"
                f"<b>🔧 ᴄᴏᴍᴍᴀɴᴅs:</b>\n\n"
                f"➻ /noabuse on  — <b>ᴇɴᴀʙʟᴇ ᴅᴇᴛᴇᴄᴛɪᴏɴ</b> ✅\n"
                f"➻ /noabuse off — <b>ᴅɪsᴀʙʟᴇ ᴅᴇᴛᴇᴄᴛɪᴏɴ</b> ❌\n\n"
                f"<b>❖ ʜᴏᴡ ɪᴛ ᴡᴏʀᴋs:</b>\n"
                f"<b>➻ ɪғ ᴀ ᴜsᴇʀ sᴇɴᴅs ᴀɴʏ ᴀʙᴜsɪᴠᴇ ᴡᴏʀᴅ, ᴛʜᴇ ᴍᴇssᴀɢᴇ ɪs ɪɴsᴛᴀɴᴛʟʏ ᴅᴇʟᴇᴛᴇᴅ.</b>\n"
                f"<b>➻ ᴛʜᴇ ᴜsᴇʀ ʀᴇᴄᴇɪᴠᴇs ᴀ 5-sᴇᴄᴏɴᴅ ᴡᴀʀɴɪɴɢ ᴍᴇssᴀɢᴇ.</b>\n\n"
                f"<b>❖ ɴᴏᴛᴇ:</b>\n"
                f"<b>➻ ᴀᴅᴍɪɴs ᴀʀᴇ ᴇxᴇᴍᴘᴛᴇᴅ ғʀᴏᴍ ᴛʜɪs ғɪʟᴛᴇʀ.</b>\n"
                f"<b>➻ ᴛʜᴇ ʙᴏᴛ ᴍᴜsᴛ ʜᴀᴠᴇ 'ᴅᴇʟᴇᴛᴇ ᴍᴇssᴀɢᴇs' ᴘᴇʀᴍɪssɪᴏɴ.</b>\n"
            )
            
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("⌯ 𝐁ᴀᴄᴋ ⌯", callback_data="help")]])
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
                f"<b>╔══════════════════╗</b>\n"
                f"<b>   🔗 ғᴏʀᴄᴇ-ꜱᴜʙꜱᴄʀɪʙᴇ</b>\n"
                f"<b>╚══════════════════╝</b>\n\n"
                f"<b>❖ ᴜsᴇʀs ᴡʜᴏ ᴅᴏ ɴᴏᴛ ᴊᴏɪɴ ʀᴇǫᴜɪʀᴇᴅ ᴄʜᴀɴɴᴇʟs ᴡɪʟʟ ʜᴀᴠᴇ</b>\n"
                f"<b>❍ ᴛʜᴇɪʀ ᴍᴇssᴀɢᴇs ᴅᴇʟᴇᴛᴇᴅ ᴀɴᴅ ʀᴇᴄᴇɪᴠᴇ ᴊᴏɪɴ ʟɪɴᴋs.</b>\n\n"
                f"<b>📢 ᴄᴏᴍᴍᴀɴᴅs:</b>\n\n"
                f"❍ /addfsub <channel> <b>➻ ᴀᴅᴅ ᴀ ᴄʜᴀɴɴᴇʟ</b>\n\n"
                f"❍ /removefsub <channel> <b>➻ ʀᴇᴍᴏᴠᴇ ᴀ ᴄʜᴀɴɴᴇʟ</b>\n\n"
                f"❍ /fsublist <b>➻ ᴠɪᴇᴡ ᴀʟʟ ᴀᴅᴅᴇᴅ ᴄʜᴀɴɴᴇʟs</b>\n\n"
                f"<b>❖ ɴᴏᴛᴇ:</b>\n"
                f"<b>➻ ᴛʜᴇ ʙᴏᴛ ᴍᴜsᴛ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ɪɴ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ.</b>\n"
                f"<b>➻ ᴡᴀʀɴɪɴɢ ᴍᴇssᴀɢᴇs ᴀʀᴇ ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇᴅ ᴀғᴛᴇʀ 30 sᴇᴄᴏɴᴅs.</b>\n\n"
                f"<b>❖ ᴇxᴀᴍᴘʟᴇ:</b>\n"
                f"➻ /addfsub @MyChannel\n"
                f"➻ /removefsub @MyChannel\n"
            )
            
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("⌯ 𝐁ᴀᴄᴋ ⌯", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=text, parse_mode=enums.ParseMode.HTML)
            await callback_query.message.edit_media(media=media, reply_markup=buttons)
            await callback_query.answer()
        except Exception as e:
            print(f"Error in fsub_help_callback: {e}")
            await callback_query.answer("❌ Something went wrong.", show_alert=True)

   #echo
    @app.on_callback_query(filters.regex("^echo_help$"))
    async def echo_help_callback(client, callback_query):
         from handlers.tools import LONGMSG_HELP_TEXT
         buttons = InlineKeyboardMarkup([[InlineKeyboardButton("⌯ 𝐁ᴀᴄᴋ ⌯", callback_data="help")]])
         media = InputMediaPhoto(media=START_IMAGE, caption=LONGMSG_HELP_TEXT, parse_mode=enums.ParseMode.HTML)
         await callback_query.message.edit_media(media=media, reply_markup=buttons)
         await callback_query.answer()

#phone
    @app.on_callback_query(filters.regex("^phone_help$"))
    async def phone_help_callback(client, callback_query):
         from handlers.tools import PHONE_HELP_TEXT
         buttons = InlineKeyboardMarkup([[InlineKeyboardButton("⌯ 𝐁ᴀᴄᴋ ⌯", callback_data="help")]])
         media = InputMediaPhoto(media=START_IMAGE, caption=PHONE_HELP_TEXT, parse_mode=enums.ParseMode.HTML)
         await callback_query.message.edit_media(media=media, reply_markup=buttons)
         await callback_query.answer()

#longmessege
    @app.on_callback_query(filters.regex("^longmsg_help$"))
    async def longmsg_help_callback(client, callback_query):
        from handlers.tools import LONGMSG_HELP_TEXT
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("⌯ 𝐁ᴀᴄᴋ ⌯", callback_data="help")]])
        media = InputMediaPhoto(media=START_IMAGE, caption=LONGMSG_HELP_TEXT, parse_mode=enums.ParseMode.HTML)
        await callback_query.message.edit_media(media=media, reply_markup=buttons)
        await callback_query.answer()

#hashtags
    @app.on_callback_query(filters.regex("^hashtag_help$"))
    async def hashtag_help_callback(client, callback_query):
        from handlers.tools import HASHTAG_HELP_TEXT
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("⌯ 𝐁ᴀᴄᴋ ⌯", callback_data="help")]])
        media = InputMediaPhoto(media=START_IMAGE, caption=HASHTAG_HELP_TEXT, parse_mode=enums.ParseMode.HTML)
        await callback_query.message.edit_media(media=media, reply_markup=buttons)
        await callback_query.answer()

    # utility help :
    @app.on_callback_query(filters.regex("^utility_help$"))
    async def utility_help_callback(client, callback_query):
        from handlers.utility import UTILITY_HELP_TEXT
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("⌯ 𝐁ᴀᴄᴋ ⌯", callback_data="help")]])
        media = InputMediaPhoto(media=START_IMAGE, caption=UTILITY_HELP_TEXT, parse_mode=enums.ParseMode.HTML)
        await callback_query.message.edit_media(media=media, reply_markup=buttons)
        await callback_query.answer()

    #command deleter :
    @app.on_callback_query(filters.regex("^cmd_help$"))
    async def cmd_help_callback(client, callback_query):
        from handlers.cmddeleter import CMDDELETER_HELP_TEXT
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("⌯ 𝐁ᴀᴄᴋ ⌯", callback_data="help")]])
        media = InputMediaPhoto(media=START_IMAGE, caption=CMDDELETER_HELP_TEXT, parse_mode=enums.ParseMode.HTML)
        await callback_query.message.edit_media(media=media, reply_markup=buttons)
        await callback_query.answer()

    # Media Deleter:
    @app.on_callback_query(filters.regex("^mediadelete_help$"))
    async def mediadelete_help_callback(client, callback_query):
        from handlers.mediadelete import MEDIADELETE_HELP_TEXT
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("⌯ 𝐁ᴀᴄᴋ ⌯", callback_data="help")]])
        media = InputMediaPhoto(media=START_IMAGE, caption=MEDIADELETE_HELP_TEXT, parse_mode=enums.ParseMode.HTML)
        await callback_query.message.edit_media(media=media, reply_markup=buttons)
        await callback_query.answer()

# Deleted Account Remover
    @app.on_callback_query(filters.regex("^zombie_help$"))
    async def zombie_help_callback(client, callback_query):
        from handlers.zombie import ZOMBIE_HELP_TEXT 
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("⌯ 𝐁ᴀᴄᴋ ⌯", callback_data="help")]])
        media = InputMediaPhoto(media=START_IMAGE, caption=ZOMBIE_HELP_TEXT, parse_mode=enums.ParseMode.HTML)
        await callback_query.message.edit_media(media=media, reply_markup=buttons)
        await callback_query.answer()

    # Tag All 
    @app.on_callback_query(filters.regex("^tagall_help$"))
    async def tagall_help_callback(client, callback_query):
        from handlers.tagall import TAGALL_HELP_TEXT
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("⌯ 𝐁ᴀᴄᴋ ⌯", callback_data="help")]])
        media = InputMediaPhoto(media=START_IMAGE, caption=TAGALL_HELP_TEXT, parse_mode=enums.ParseMode.HTML)
        await callback_query.message.edit_media(media=media, reply_markup=buttons)
        await callback_query.answer()


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
