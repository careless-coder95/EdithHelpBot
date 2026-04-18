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
            f"<blockquote>"
            f"<b>✨ 𝐇ᴇʏ {user} 🤍 </b>\n"
            f"<b>❍ ɪ’ᴍ 𝙴𝙳𝙸𝚃𝙷 🤖 — ʏᴏᴜʀ sᴍᴧʀᴛ ɢʀᴏᴜᴘ ʜᴇʟᴘ ʙᴏᴛ.</b>"
            f"</blockquote>\n"
            f"<blockquote expandable>"
            f"<b>❖ 𝐇𝐈𝐆𝐇𝐋𝐈𝐆𝐇𝐓𝐒 ❖</b>\n"
            f"<b>➻ sᴍᴀʀᴛ ᴀɴᴛɪ-sᴘᴀᴍ & ʟɪɴᴋ sʜɪᴇʟᴅ</b>\n"
            f"<b>➻ ᴀᴅᴀᴘᴛɪᴠᴇ ʟᴏᴄᴋ sʏsᴛᴇᴍ 🔒</b>\n"
            f"<b>➻ ʙɪᴏʟɪɴᴋ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ 🛡️</b>\n"
            f"<b>➻ ɴᴏᴛᴇs & ʀᴜʟᴇs ᴍᴀɴᴀɢᴇᴍᴇɴᴛ 📌</b>\n"
            f"<b>✦ ꜰᴀsᴛ ✦ sᴇᴄᴜʀᴇ ✦ ʀᴇʟɪᴀʙʟᴇ ✦</b>"
            f"</blockquote>"
        )
        )
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("✙ 𝐀ᴅᴅ 𝐌є 𝐈η 𝐘συʀ 𝐆ʀσυᴘ ✙", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
            [
                InlineKeyboardButton("⌯ 𝐒ᴜᴘᴘσʀᴛ ⌯", url=SUPPORT_GROUP),
                InlineKeyboardButton("⌯ 𝐔ᴘᴅᴀᴛᴇ ⌯", url=UPDATE_CHANNEL),
            ],
            [
                InlineKeyboardButton("⌯ 𝐌ʏ 𝐌ᴧsᴛᴇʀ ⌯", url=f"tg://user?id={OWNER_ID}"),
                InlineKeyboardButton("🌍 Language", callback_data="lang_help"),
            ],
            [InlineKeyboardButton("⌯ 𝐇єʟᴘ 𝐀ηᴅ 𝐂ᴏᴍᴍᴧηᴅ𝐬 ⌯", callback_data="help")]
        ])

        if message.text:
            await message.reply_photo(
                START_IMAGE,
                caption=text,
                reply_markup=buttons,
                parse_mode=enums.ParseMode.HTML
            )
        else:
            media = InputMediaPhoto(
                media=START_IMAGE,
                caption=text,
                parse_mode=enums.ParseMode.HTML
            )
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
                return await message.reply_text(f"⚠️ Note <code>#{name}</code> not found or deleted.", parse_mode=enums.ParseMode.HTML)

            return await message.reply_text(
                f"╔════════════════════════╗\n"
                f"   📝 𝙽𝙾𝚃𝙴: <b>#{name}</b>\n"
                f"╚════════════════════════╝\n\n"
                f"{content}",
                parse_mode=enums.ParseMode.HTML
            )

        user = message.from_user
        await db.add_user(user.id, user.first_name)
        await send_start_menu(message, user.first_name)


    # ==========================================================
    # Help Menu — Paginated (8 buttons per page, 2x4 grid)
    # ==========================================================

    ALL_HELP_BUTTONS = [
        ("💌 𝐆ʀᴇᴇᴛɪɴɢs ⌯", "greetings"),
        ("🔐 𝐋ᴏcᴋs ⌯", "locks"),
        ("🔮 𝐌ᴏᴅʀᴀᴛɪᴏɴ ⌯", "moderation"),
        ("🔗 𝐁ɪᴏ 𝐋ɪɴᴋ ⌯", "biolink"),
        ("📝 𝐍ᴏᴛᴇs ⌯", "notes_help"),
        ("📑 𝐑ᴜʟᴇs ⌯", "rules_help"),
        ("🤬 𝐀ʙᴜsᴇ ⌯", "abuse_help"),
        ("🪠 𝐅-𝐒ᴜʙ ⌯", "fsub_help"),
        ("🚧 𝐄cʜᴏ ⌯", "echo_help"),
        ("📵 𝐏ʜᴏɴᴇ ⌯", "phone_help"),
        ("⌛ 𝐋ᴏɴɢ 𝐋ɪᴍɪᴛ ⌯", "longmsg_help"),
        ("#️⃣ 𝐇ᴀsʜᴛᴀɢ ⌯", "hashtag_help"),
        ("⚙️ 𝐔ᴛɪʟɪᴛʏ ⌯", "utility_help"),
        ("🗑️ 𝐂ᴍᴅ 𝐃ᴇʟᴇᴛᴇʀ ⌯", "cmd_help"),
        ("🚮 𝐌ᴇᴅɪᴀ 𝐃ᴇʟᴇᴛᴇʀ ⌯", "mediadelete_help"),
        ("🧴 𝐂ʟᴇᴀɴᴇʀ ⌯", "cleaner_help"),
        ("🧟 𝐙ᴏᴍʙɪᴇs ⌯", "zombie_help"),
        ("🔖 𝐓ᴀɢ 𝐀ʟʟ ⌯", "tagall_help"),
        ("👮🏻 𝐏ʀᴏᴍᴏᴛᴇ ⌯", "promote_help"),
        ("🚫 𝐁ʟᴀcᴋʟɪsᴛ ⌯", "blacklist_help"),
        ("🤿 𝐅ɪʟᴛᴇʀs ⌯", "filters_help"),
        ("⛩️ 𝐉ᴏɪɴ 𝐑ᴇǫᴜᴇsᴛ ⌯", "joinrequest_help"),
    ]

    BUTTONS_PER_PAGE = 8
    TOTAL_PAGES = (len(ALL_HELP_BUTTONS) + BUTTONS_PER_PAGE - 1) // BUTTONS_PER_PAGE


    def build_help_page(page: int):
        start = page * BUTTONS_PER_PAGE
        end = start + BUTTONS_PER_PAGE
        page_buttons = ALL_HELP_BUTTONS[start:end]

        # 2 buttons per row — 4 rows = 8 buttons
        rows = []
        for i in range(0, len(page_buttons), 2):
            pair = page_buttons[i:i+2]
            rows.append([InlineKeyboardButton(label, callback_data=cb) for label, cb in pair])

        # Nav row — Prev | Back | Next
        nav = []
        if page > 0:
            nav.append(InlineKeyboardButton("◀ 𝐏𝐫𝐞𝐯", callback_data=f"helppage_{page - 1}"))
        else:
            nav.append(InlineKeyboardButton("◀", callback_data="noop"))

        nav.append(InlineKeyboardButton("🏠 𝐁𝐚𝐜𝐤", callback_data="back_to_start"))

        if page < TOTAL_PAGES - 1:
            nav.append(InlineKeyboardButton("𝐍𝐞𝐱𝐭 ▶", callback_data=f"helppage_{page + 1}"))
        else:
            nav.append(InlineKeyboardButton("▶", callback_data="noop"))

        rows.append(nav)

        text = (
            f"<b>❖ ᴄʜσσsє ᴛʜє ᴄᴧᴛєɢσʀʏ ғσʀ ᴡʜɪᴄʜ ʏσυ ᴡᴧηηᴧ ɢєᴛ ʜєʟᴩ</b>\n\n"
            f"<b>➥ ᴧsᴋ ʏσυʀ ᴅσυʙᴛs ᴧᴛ sυᴘᴘσʀᴛ ᴄʜᴧᴛ</b>\n"
            f"<b>ᴧʟʟ ᴄσϻϻᴧηᴅs ᴄᴧη ʙє υsєᴅ ᴡɪᴛʜ :</b><code>/</code>"
        )
        return text, InlineKeyboardMarkup(rows)


    async def send_help_menu(message, page=0):
        text, buttons = build_help_page(page)
        media = InputMediaPhoto(
            media=START_IMAGE,
            caption=text,
            parse_mode=enums.ParseMode.HTML
        )
        await message.edit_media(media=media, reply_markup=buttons)


    # ==========================================================
    # help callback
    # ==========================================================
    @app.on_callback_query(filters.regex("^help$"))
    async def help_callback(client, callback_query):
        await send_help_menu(callback_query.message, page=0)
        await callback_query.answer()


    # ==========================================================
    # helppage_N callback
    # ==========================================================
    @app.on_callback_query(filters.regex(r"^helppage_(\d+)$"))
    async def helppage_callback(client, callback_query):
        page = int(callback_query.matches[0].group(1))
        await send_help_menu(callback_query.message, page=page)
        await callback_query.answer()


    # ==========================================================
    # noop — disabled nav button
    # ==========================================================
    @app.on_callback_query(filters.regex("^noop$"))
    async def noop_callback(client, callback_query):
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
            f"<b>⚙ ᴡᴇʟᴄᴏᴍᴇ sʏsᴛᴇᴍ</b>\n"
            f"<b>╚══════════════════╝</b>\n\n"
    
            f"<b>❖ ᴄᴏᴍᴍᴧɴᴅs ❖</b>\n\n"
            f"<b>➻ /setwelcome &lt;ᴛᴇxᴛ&gt; — sᴇᴛ ᴄᴜsᴛᴏᴍ ᴡᴇʟᴄᴏᴍᴇ</b>\n"
            f"<b>➻ /welcome on — ᴇɴᴧʙʟᴇ ᴡᴇʟᴄᴏᴍᴇ</b>\n"
            f"<b>➻ /welcome off— ᴅɪsᴧʙʟᴇ ᴡᴇʟᴄᴏᴍᴇ</b>\n\n"
            f"<b>❖ ᴘʟᴧᴄᴇʜᴏʟᴅᴇʀs ❖</b>\n"
            f"<b><code>{{username}}</code> — ᴛᴇʟᴇɢʀᴧᴍ ᴜsᴇʀɴᴧᴍᴇ</b>\n"
            f"<b><code>{{first_name}}</code> — ᴜsᴇʀ's ғɪʀsᴛ ɴᴧᴍᴇ</b>\n"
            f"<b><code>{{mention}}</code> — ᴍᴇɴᴛɪᴏɴ ᴜsᴇʀ</b>\n"
            f"<b><code>{{title}}</code> — ɢʀᴏᴜᴘ ᴛɪᴛʟᴇ</b>\n\n"
    
            f"<b>❖ ᴇxᴧᴍᴘʟᴇ ❖</b>\n"
            f"<b><code>/setwelcome ʜᴇʟʟᴏ {{first_name}}! ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ {{title}}!</code></b>"
        )

        
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("⌯ 𝐁𝐚𝐜𝐤 ⌯", callback_data="help")]])
        media = InputMediaPhoto(media=START_IMAGE, caption=text, parse_mode=enums.ParseMode.HTML)
        await callback_query.message.edit_media(media=media, reply_markup=buttons)
        await callback_query.answer()


    # ==========================================================
    # Locks callback
    # ==========================================================
    @app.on_callback_query(filters.regex("^locks$"))
    async def locks_callback(client, callback_query):
        text = (
    f"<blockquote expandable>"
    f"<b>╔══════════════════╗</b>\n"
    f"<b>⚙ ʟᴏᴄᴋs sʏsᴛᴇᴍ</b>\n"
    f"<b>╚══════════════════╝</b>\n\n"
    
    f"<b>❖ ᴄᴏᴍᴍᴧɴᴅs ❖</b>\n\n"
    f"<b>➻ /lock &lt;type&gt; — ᴇɴᴧʙʟᴇ ᴧ ʟᴏᴄᴋ</b>\n"
    f"<b>➻ /unlock &lt;type&gt; — ᴅɪsᴧʙʟᴇ ᴧ ʟᴏᴄᴋ</b>\n"
    f"<b>➻ /locks — sʜᴏᴡ ᴧᴄᴛɪᴠᴇ ʟᴏᴄᴋs</b>\n"
    f"<b>➻ /lockall — ʟᴏᴄᴋ ᴇᴠᴇʀʏᴛʜɪɴɢ 🔐</b>\n"
    f"<b>➻ /unlockall — ᴜɴʟᴏᴄᴋ ᴇᴠᴇʀʏᴛʜɪɴɢ 🔓</b>\n\n"
    
    f"<b>❖ ᴧᴠᴧɪʟᴧʙʟᴇ ᴛʏᴘᴇs ❖</b>\n"
    f"<b><code>url</code> • <code>text</code> • <code>sticker</code> • <code>media</code></b>\n"
    f"<b><code>username</code> • <code>forward</code> • <code>edit</code></b>"
    f"</blockquote>"
        )
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("⌯ 𝐁𝐚𝐜𝐤 ⌯", callback_data="help")]])
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
    f"<blockquote expandable>"
    f"<b>╔══════════════════╗</b>\n"
    f"<b>⚙️ ᴍᴏᴅᴇʀᴧᴛɪᴏɴ</b>\n"
    f"<b>╚══════════════════╝</b>\n\n"
    
    f"<b>➻ /kick &lt;user&gt; — ʀᴇᴍᴏᴠᴇ ᴧ ᴜsᴇʀ</b>\n"
    f"<b>➻ /ban &lt;user&gt; — ʙᴧɴ ᴘᴇʀᴍᴧɴᴇɴᴛʟʏ</b>\n"
    f"<b>➻ /unban &lt;user&gt; — ʟɪғᴛ ʙᴧɴ</b>\n"
    f"<b>➻ /mute &lt;user&gt; — ᴅɪsᴧʙʟᴇ ᴍᴇssᴧɢᴇs</b>\n"
    f"<b>➻ /unmute &lt;user&gt; — ᴧʟʟᴏᴡ ᴍᴇssᴧɢᴇs ᴧɢᴧɪɴ</b>\n"
    f"<b>➻ /tmute &lt;user&gt; &lt;time&gt; — ᴛᴇᴍᴘ ᴍᴜᴛᴇ (1ᴍ–24ʜ)</b>\n"
    f"<b>➻ /tban &lt;user&gt; &lt;time&gt; — ᴛᴇᴍᴘ ʙᴧɴ (1ᴍ–24ʜ)</b>\n"
    f"<b>➻ /warn &lt;user&gt; — ᴡᴧʀɴɪɴɢ (3 = ᴍᴜᴛᴇ)</b>\n"
    f"<b>➻ /warns &lt;user&gt; — ᴠɪᴇᴡ ᴡᴧʀɴɪɴɢs</b>\n"
    f"<b>➻ /resetwarns &lt;user&gt; — ᴄʟᴇᴧʀ ᴡᴧʀɴɪɴɢs</b>\n\n"
    
    f"<b><i>ʀᴇᴘʟʏ ᴛᴏ ᴧ ᴜsᴇʀ ᴏʀ ᴛʏᴘᴇ /ban @username</i></b>"
    f"</blockquote>"
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("⌯ 𝐁𝐚𝐜𝐤 ⌯", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=text, parse_mode=enums.ParseMode.HTML)
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
            text = (
    f"<blockquote expandable>"
    f"<b>╔══════════════════╗</b>\n"
    f"<b>🔗 ʙɪᴏʟɪɴᴋ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ</b>\n"
    f"<b>╚══════════════════╝</b>\n\n"
    
    f"<b>ʙʟᴏᴄᴋs ᴜsᴇʀs ᴡʜᴏ ʜᴧᴠᴇ ʟɪɴᴋs ɪɴ ᴛʜᴇɪʀ ʙɪᴏ.</b>\n\n"
    
    f"<b>❖ ᴄᴏᴍᴍᴧɴᴅs ❖</b>\n\n"
    f"<b>➻ /biolink on — ᴘʀᴏᴛᴇᴄᴛɪᴏɴ ᴏɴ ✅</b>\n"
    f"<b>➻ /biolink off — ᴘʀᴏᴛᴇᴄᴛɪᴏɴ ᴏғғ ❌</b>\n\n"
    
    f"<b>❖ ɴᴏᴛᴇs ❖</b>\n"
    f"<b>➻ ʙɪᴏ ʟɪɴᴋ ᴅᴇᴛᴇᴄᴛᴇᴅ → ᴍᴇssᴧɢᴇ ᴅᴇʟᴇᴛᴇᴅ</b>\n"
    f"<b>➻ ᴧᴅᴍɪɴs ᴧʀᴇ ɴᴏᴛ ᴧғғᴇᴄᴛᴇᴅ</b>\n"
    f"<b>➻ ʙᴏᴛ ɴᴇᴇᴅs ᴅᴇʟᴇᴛᴇ ᴍᴇssᴧɢᴇs ᴘᴇʀᴍɪssɪᴏɴ</b>"
    f"</blockquote>"
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("⌯ 𝐁𝐚𝐜𝐤 ⌯", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=text, parse_mode=enums.ParseMode.HTML)
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
            text = (
    f"<blockquote expandable>"
    f"<b>╔════════════════════════╗</b>\n"
    f"<b>📝 ɴᴏᴛᴇs</b>\n"
    f"<b>╚════════════════════════╝</b>\n\n"
    
    f"<b>❖ 👮 ᴧᴅᴍɪɴ ᴄᴏᴍᴍᴧɴᴅs ❖</b>\n"
    f"<b>➻ /setnote &lt;name&gt; &lt;content&gt;</b>\n"
    f"<b>➻ /delnote &lt;name&gt;</b>\n\n"
    
    f"<b>❖ 👥 ᴜsᴇʀ ᴄᴏᴍᴍᴧɴᴅs ❖</b>\n"
    f"<b>➻ /notes — ʟɪsᴛ ᴧʟʟ ɴᴏᴛᴇs</b>\n"
    f"<b>➻ #note_name — ɢᴇᴛ ᴘʀɪᴠᴧᴛᴇ ʟɪɴᴋ</b>\n\n"
    
    f"<b><i>ᴇᴧᴄʜ ɴᴏᴛᴇ ᴏᴘᴇɴs ɪɴ ᴘʀɪᴠᴧᴛᴇ ᴄʜᴧᴛ ᴠɪᴧ ʟɪɴᴋ</i></b>"
    f"</blockquote>"
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("⌯ 𝐁𝐚𝐜𝐤 ⌯", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=text, parse_mode=enums.ParseMode.HTML)
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
            text = (
    f"<blockquote expandable>"
    f"<b>╔══════════════════╗</b>\n"
    f"<b>📜 ʀᴜʟᴇs</b>\n"
    f"<b>╚══════════════════╝</b>\n\n"
    
    f"<b>❖ ᴄᴏᴍᴍᴧɴᴅs ❖</b>\n\n"
    f"<b>➻ /setrules &lt;text&gt; — sᴇᴛ ɢʀᴏᴜᴘ ʀᴜʟᴇs</b>\n"
    f"<b>➻ /rules — sʜᴏᴡ ᴄᴜʀʀᴇɴᴛ ʀᴜʟᴇs</b>\n"
    f"<b>➻ /clearrules — ʀᴇᴍᴏᴠᴇ ᴧʟʟ ʀᴜʟᴇs</b>\n\n"
    
    f"<b>➻ 🌟 ғᴏʀᴍᴧᴛᴛɪɴɢ ɪs ᴘʀᴇsᴇʀᴠᴇᴅ ᴇxᴧᴄᴛʟʏ ᴧs ᴛʏᴘᴇᴅ</b>"
    f"</blockquote>"
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("⌯ 𝐁𝐚𝐜𝐤 ⌯", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=text, parse_mode=enums.ParseMode.HTML)
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
            text = (
    f"<blockquote expandable>"
    f"<b>╔══════════════════╗</b>\n"
    f"<b>🤬 ᴧʙᴜsᴇ ᴅᴇᴛᴇᴄᴛɪᴏɴ</b>\n"
    f"<b>╚══════════════════╝</b>\n\n"
    
    f"<b>ᴧʙᴜsɪᴠᴇ ᴍᴇssᴧɢᴇs ᴧʀᴇ ᴧᴜᴛᴏᴍᴧᴛɪᴄᴧʟʟʏ ᴅᴇʟᴇᴛᴇᴅ.</b>\n\n"
    
    f"<b>❖ ᴄᴏᴍᴍᴧɴᴅs ❖</b>\n\n"
    f"<b>➻ /noabuse on — ᴇɴᴧʙʟᴇ ✅</b>\n"
    f"<b>➻ /noabuse off — ᴅɪsᴧʙʟᴇ ❌</b>\n\n"
    
    f"<b>❖ ɴᴏᴛᴇs ❖</b>\n"
    f"<b>➻ ᴍᴇssᴧɢᴇ ᴅᴇʟᴇᴛᴇᴅ ɪɴsᴛᴧɴᴛʟʏ</b>\n"
    f"<b>➻ 5 sᴇᴄᴏɴᴅ ᴡᴧʀɴɪɴɢ sᴇɴᴛ</b>\n"
    f"<b>➻ ᴧᴅᴍɪɴs ɴᴏᴛ ᴧғғᴇᴄᴛᴇᴅ</b>"
    f"</blockquote>"
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("⌯ 𝐁𝐚𝐜𝐤 ⌯", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=text, parse_mode=enums.ParseMode.HTML)
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
            text = (
    f"<blockquote expandable>"
    f"<b>╔══════════════════╗</b>\n"
    f"<b>🔗 ғᴏʀᴄᴇ-sᴜʙsᴄʀɪʙᴇ</b>\n"
    f"<b>╚══════════════════╝</b>\n\n"
    
    f"<b>ᴜsᴇʀs ᴡʜᴏ ʜᴧᴠᴇɴ'ᴛ ᴊᴏɪɴᴇᴅ ʀᴇǫᴜɪʀᴇᴅ</b>\n"
    f"<b>ᴄʜᴧɴɴᴇʟs ᴄᴧɴɴᴏᴛ sᴇɴᴅ ᴍᴇssᴧɢᴇs.</b>\n\n"
    
    f"<b>❖ ᴄᴏᴍᴍᴧɴᴅs ❖</b>\n\n"
    f"<b>➻ /addfsub @channel — ᴧᴅᴅ ᴄʜᴧɴɴᴇʟ</b>\n"
    f"<b>➻ /removefsub @channel — ʀᴇᴍᴏᴠᴇ ᴄʜᴧɴɴᴇʟ</b>\n"
    f"<b>➻ /fsublist — ʟɪsᴛ ᴄʜᴧɴɴᴇʟs</b>\n\n"
    
    f"<b><i>ʙᴏᴛ ᴍᴜsᴛ ʙᴇ ᴧᴅᴍɪɴ ɪɴ ᴛʜᴇ ᴄʜᴧɴɴᴇʟ</i></b>"
    f"</blockquote>"
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("⌯ 𝐁𝐚𝐜𝐤 ⌯", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=text, parse_mode=enums.ParseMode.HTML)
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
            text = (
    f"<blockquote expandable>"
    f"<b>╔══════════════════╗</b>\n"
    f"<b>📄 ʟᴏɴɢ ᴍᴇssᴧɢᴇ</b>\n"
    f"<b>╚══════════════════╝</b>\n\n"
    
    f"<b>ʟᴏɴɢ ᴍᴇssᴧɢᴇs ᴧʀᴇ ᴜᴘʟᴏᴧᴅᴇᴅ ᴛᴏ ᴛᴇʟᴇɢʀᴧᴘʜ</b>\n"
    f"<b>ᴧɴᴅ sᴇɴᴛ ᴧs ᴧ ʟɪɴᴋ ᴧᴜᴛᴏᴍᴧᴛɪᴄᴧʟʟʏ.</b>\n\n"
    
    f"<b>❖ ᴄᴏᴍᴍᴧɴᴅs ❖</b>\n\n"
    f"<b>➻ /echo &lt;text&gt; — ᴇᴄʜᴏ ᴛᴇxᴛ</b>\n"
    f"<b>➻ /setlongmode off — ɴᴏ ᴧᴄᴛɪᴏɴ</b>\n"
    f"<b>➻ /setlongmode manual — ᴅᴇʟᴇᴛᴇ + ᴡᴧʀɴ</b>\n"
    f"<b>➻ /setlongmode automatic — ᴅᴇʟᴇᴛᴇ + ʟɪɴᴋ ✅</b>\n"
    f"<b>➻ /setlonglimit &lt;200–4000&gt; — sᴇᴛ ʟɪᴍɪᴛ</b>\n\n"
    
    f"<b><i>ᴅᴇғᴧᴜʟᴛ ʟɪᴍɪᴛ: 800 ᴄʜᴧʀᴧᴄᴛᴇʀs</i></b>"
    f"</blockquote>"
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("⌯ 𝐁𝐚𝐜𝐤 ⌯", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=text, parse_mode=enums.ParseMode.HTML)
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
            text = (
    f"<blockquote expandable>"
    f"<b>╔══════════════════╗</b>\n"
    f"<b>📞 ᴘʜᴏɴᴇ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ</b>\n"
    f"<b>╚══════════════════╝</b>\n\n"
    
    f"<b>ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀs ɪɴ ᴍᴇssᴧɢᴇs ᴧʀᴇ</b>\n"
    f"<b>ᴧᴜᴛᴏᴍᴧᴛɪᴄᴧʟʟʏ ᴅᴇʟᴇᴛᴇᴅ.</b>\n\n"
    
    f"<b>❖ ᴄᴏᴍᴍᴧɴᴅs ❖</b>\n\n"
    f"<b>➻ /nophone on — ʙʟᴏᴄᴋ ✅</b>\n"
    f"<b>➻ /nophone off — ᴧʟʟᴏᴡ ❌</b>\n\n"
    
    f"<b>❖ ᴅᴇᴛᴇᴄᴛɪᴏɴ ❖</b>\n"
    f"<b>➻ +91 9876543210</b>\n"
    f"<b>➻ +1-234-567-8900</b>\n"
    f"<b>➻ 919876543210</b>"
    f"</blockquote>"
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("⌯ 𝐁𝐚𝐜𝐤 ⌯", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=text, parse_mode=enums.ParseMode.HTML)
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
            text = (
    f"<blockquote expandable>"
    f"<b>╔══════════════════╗</b>\n"
    f"<b>📄 ʟᴏɴɢ ᴍᴇssᴧɢᴇ</b>\n"
    f"<b>╚══════════════════╝</b>\n\n"
    
    f"<b>ʟᴏɴɢ ᴍᴇssᴧɢᴇs ᴧʀᴇ ᴜᴘʟᴏᴧᴅᴇᴅ ᴛᴏ ᴛᴇʟᴇɢʀᴧᴘʜ</b>\n"
    f"<b>ᴧɴᴅ sᴇɴᴛ ᴧs ᴧ ʟɪɴᴋ ᴧᴜᴛᴏᴍᴧᴛɪᴄᴧʟʟʏ.</b>\n\n"
    
    f"<b>❖ ᴄᴏᴍᴍᴧɴᴅs ❖</b>\n\n"
    f"<b>➻ /echo &lt;text&gt; — ᴇᴄʜᴏ ᴛᴇxᴛ</b>\n"
    f"<b>➻ /setlongmode off — ɴᴏ ᴧᴄᴛɪᴏɴ</b>\n"
    f"<b>➻ /setlongmode manual — ᴅᴇʟᴇᴛᴇ + ᴡᴧʀɴ</b>\n"
    f"<b>➻ /setlongmode automatic — ᴅᴇʟᴇᴛᴇ + ʟɪɴᴋ ✅</b>\n"
    f"<b>➻ /setlonglimit &lt;200–4000&gt; — sᴇᴛ ʟɪᴍɪᴛ</b>\n\n"
    
    f"<b><i>ᴅᴇғᴧᴜʟᴛ ʟɪᴍɪᴛ: 800 ᴄʜᴧʀᴧᴄᴛᴇʀs</i></b>"
    f"</blockquote>"
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("⌯ 𝐁𝐚𝐜𝐤 ⌯", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=text, parse_mode=enums.ParseMode.HTML)
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
            text = (
    f"<blockquote expandable>"
    f"<b>╔══════════════════╗</b>\n"
    f"<b># ʜᴧsʜᴛᴧɢ ғɪʟᴛᴇʀ</b>\n"
    f"<b>╚══════════════════╝</b>\n\n"
    
    f"<b>ʜᴧsʜᴛᴧɢ ᴍᴇssᴧɢᴇs ᴧʀᴇ ᴧᴜᴛᴏᴍᴧᴛɪᴄᴧʟʟʏ ᴅᴇʟᴇᴛᴇᴅ.</b>\n\n"
    
    f"<b>❖ ᴄᴏᴍᴍᴧɴᴅs ❖</b>\n\n"
    f"<b>➻ /nohashtags on — ʙʟᴏᴄᴋ ✅</b>\n"
    f"<b>➻ /nohashtags off — ᴧʟʟᴏᴡ ❌</b>\n\n"
    
    f"<b>❖ ᴅᴇᴛᴇᴄᴛɪᴏɴ ❖</b>\n"
    f"<b>➻ #join, #promotion, #trending</b>\n"
    f"<b>➻ ᴧɴʏ ᴡᴏʀᴅ sᴛᴧʀᴛɪɴɢ ᴡɪᴛʜ #</b>"
    f"</blockquote>"
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("⌯ 𝐁𝐚𝐜𝐤 ⌯", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=text, parse_mode=enums.ParseMode.HTML)
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
            text = (
    f"<blockquote expandable>"
    f"<b>╔══════════════════╗</b>\n"
    f"<b>⚙️ ᴜᴛɪʟɪᴛʏ</b>\n"
    f"<b>╚══════════════════╝</b>\n\n"
    
    f"<b>➻ /chatinfo — ɢʀᴏᴜᴘ ᴅᴇᴛᴧɪʟs &amp; ᴍᴇᴍʙᴇʀ ᴄᴏᴜɴᴛ</b>\n"
    f"<b>➻ /id — ʏᴏᴜʀ ɪᴅ ᴏʀ ʀᴇᴘʟɪᴇᴅ ᴜsᴇʀ's ɪᴅ</b>\n"
    f"<b>➻ /pin — ᴘɪɴ ᴧ ʀᴇᴘʟɪᴇᴅ ᴍᴇssᴧɢᴇ</b>\n"
    f"<b>➻ /unpin — ᴜɴᴘɪɴ ᴍᴇssᴧɢᴇ ᴏʀ ᴧʟʟ ᴘɪɴs</b>\n"
    f"<b>➻ /purge — ʙᴜʟᴋ ᴅᴇʟᴇᴛᴇ ᴍᴇssᴧɢᴇs</b>\n"
    f"<b>➻ /del — ᴅᴇʟᴇᴛᴇ ᴧ ʀᴇᴘʟɪᴇᴅ ᴍᴇssᴧɢᴇ</b>\n"
    f"<b>➻ /report — ʀᴇᴘᴏʀᴛ ᴧ ᴜsᴇʀ ᴛᴏ ᴧᴅᴍɪɴs</b>\n\n"
    
    f"<b><i>ᴘɪɴ, ᴘᴜʀɢᴇ, ᴅᴇʟ — ᴧᴅᴍɪɴ ᴏɴʟʏ</i></b>"
    f"</blockquote>"
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("⌯ 𝐁𝐚𝐜𝐤 ⌯", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=text, parse_mode=enums.ParseMode.HTML)
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
            text = (
    f"<blockquote expandable>"
    f"<b>╔══════════════════╗</b>\n"
    f"<b>🗑️ ᴄᴍᴅ ᴅᴇʟᴇᴛᴇʀ</b>\n"
    f"<b>╚══════════════════╝</b>\n\n"
    
    f"<b>ᴄᴏᴍᴍᴧɴᴅs sᴛᴀʀᴛɪɴɢ ᴡɪᴛʜ <code>/</code> <code>!</code> <code>.</code></b>\n"
    f"<b>ᴀʀᴇ ᴀᴜᴛᴏᴍᴧᴛɪᴄᴧʟʟʏ ᴅᴇʟᴇᴛᴇᴅ.</b>\n\n"
    
    f"<b>❖ ᴄᴏᴍᴍᴧɴᴅs ❖</b>\n\n"
    f"<b>➻ /cmd on — ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴏɴ ✅</b>\n"
    f"<b>➻ /cmd off — ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴏғғ ❌</b>\n\n"
    
    f"<b><i>ᴀᴅᴍɪɴs ᴀʀᴇ ɴᴏᴛ ᴀғғᴇᴄᴛᴇᴅ.</i></b>"
    f"</blockquote>"
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("⌯ 𝐁𝐚𝐜𝐤 ⌯", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=text, parse_mode=enums.ParseMode.HTML)
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
            text = (
    f"<blockquote expandable>"
    f"<b>╔══════════════════╗</b>\n"
    f"<b>🎬 ᴍᴇᴅɪᴧ ᴧᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ</b>\n"
    f"<b>╚══════════════════╝</b>\n\n"
    
    f"<b>ᴍᴇᴅɪᴧ ᴍᴇssᴧɢᴇs ᴧʀᴇ ᴧᴜᴛᴏᴍᴧᴛɪᴄᴧʟʟʏ ᴅᴇʟᴇᴛᴇᴅ</b>\n"
    f"<b>ᴧғᴛᴇʀ ᴧ ᴄᴏɴғɪɢᴜʀᴇᴅ ᴅᴇʟᴧʏ.</b>\n\n"
    
    f"<b>❖ ᴄᴏᴍᴍᴧɴᴅs ❖</b>\n\n"
    f"<b>➻ /mediadelete on — ᴇɴᴧʙʟᴇ ✅</b>\n"
    f"<b>➻ /mediadelete off — ᴅɪsᴧʙʟᴇ ❌</b>\n"
    f"<b>➻ /setmediadelay &lt;time&gt; — sᴇᴛ ᴅᴇʟᴧʏ</b>\n\n"
    
    f"<b>❖ ᴧᴘᴘʟɪᴇs ᴛᴏ ❖</b>\n"
    f"<b>➻ ᴘʜᴏᴛᴏs, ᴠɪᴅᴇᴏs, sᴛɪᴄᴋᴇʀs, ɢɪғs</b>\n"
    f"<b>➻ ᴧɴɪᴍᴧᴛɪᴏɴs, ʟᴏᴄᴧᴛɪᴏɴs, ᴘᴏʟʟs</b>\n\n"
    
    f"<b><i>ʀᴧɴɢᴇ: 1ᴍ ᴛᴏ 24ʜ — ᴅᴇғᴧᴜʟᴛ: 5ᴍ</i></b>"
    f"</blockquote>"
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("⌯ 𝐁𝐚𝐜𝐤 ⌯", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=text, parse_mode=enums.ParseMode.HTML)
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
            text = (
    f"<blockquote expandable>"
    f"<b>╔══════════════════╗</b>\n"
    f"<b>🧹 ᴍᴇssᴧɢᴇ ᴄʟᴇᴧɴᴇʀ</b>\n"
    f"<b>╚══════════════════╝</b>\n\n"
    
    f"<b>ᴧʟʟ ʀᴇɢᴜʟᴧʀ ᴜsᴇʀ ᴍᴇssᴧɢᴇs ᴧʀᴇ ᴅᴇʟᴇᴛᴇᴅ</b>\n"
    f"<b>ᴧᴜᴛᴏᴍᴧᴛɪᴄᴧʟʟʏ ᴧғᴛᴇʀ ᴧ sᴇᴛ ᴅᴇʟᴧʏ.</b>\n\n"
    
    f"<b>❖ ᴄᴏᴍᴍᴧɴᴅs ❖</b>\n\n"
    f"<b>➻ /cleaner on — ᴇɴᴧʙʟᴇ ✅</b>\n"
    f"<b>➻ /cleaner off — ᴅɪsᴧʙʟᴇ ❌</b>\n"
    f"<b>➻ /setcleandelay &lt;time&gt; — sᴇᴛ ᴅᴇʟᴧʏ</b>\n"
    f"<b>➻ /cleanstatus — sʜᴏᴡ sᴇᴛᴛɪɴɢs</b>\n\n"
    
    f"<b>❖ ɴᴏᴛᴇs ❖</b>\n"
    f"<b>➻ ᴧᴅᴍɪɴ ᴍᴇssᴧɢᴇs ᴧʀᴇ ɴᴇᴠᴇʀ ᴅᴇʟᴇᴛᴇᴅ</b>\n"
    f"<b>➻ ʀᴧɴɢᴇ: 1ᴍ ᴛᴏ 24ʜ — ᴅᴇғᴧᴜʟᴛ: 5ᴍ</b>"
    f"</blockquote>"
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("⌯ 𝐁𝐚𝐜𝐤 ⌯", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=text, parse_mode=enums.ParseMode.HTML)
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
            text = (
    f"<blockquote expandable>"
    f"<b>╔════════════════════╗</b>\n"
    f"<b>⚠️ ᴢᴏᴍʙɪᴇ ʀᴇᴍᴏᴠᴇʀ</b>\n"
    f"<b>╚════════════════════╝</b>\n\n"
    
    f"<b>sᴄᴧɴs ᴧɴᴅ ʀᴇᴍᴏᴠᴇs ᴧʟʟ ᴅᴇʟᴇᴛᴇᴅ ᴛᴇʟᴇɢʀᴧᴍ</b>\n"
    f"<b>ᴧᴄᴄᴏᴜɴᴛs ғʀᴏᴍ ᴛʜᴇ ɢʀᴏᴜᴘ.</b>\n\n"
    
    f"<b>❖ ᴄᴏᴍᴍᴧɴᴅs ❖</b>\n\n"
    f"<b>➻ /zombie — sᴄᴧɴ &amp; ʀᴇᴍᴏᴠᴇ ᴅᴇʟᴇᴛᴇᴅ ᴧᴄᴄᴏᴜɴᴛs</b>\n\n"
    
    f"<b>❖ ɴᴏᴛᴇs ❖</b>\n"
    f"<b>➻ ʙᴏᴛ ᴍᴜsᴛ ʙᴇ ᴧᴅᴍɪɴ ᴡɪᴛʜ ʙᴧɴ ᴘᴇʀᴍɪssɪᴏɴ</b>\n"
    f"<b>➻ ᴏɴʟʏ ᴧᴅᴍɪɴs ᴄᴧɴ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴧɴᴅ</b>"
    f"</blockquote>"
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("⌯ 𝐁𝐚𝐜𝐤 ⌯", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=text, parse_mode=enums.ParseMode.HTML)
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
            text = (
    f"<blockquote expandable>"
    f"<b>╔════════════════════════╗</b>\n"
    f"<b>📢 ᴛᴧɢ ᴧʟʟ</b>\n"
    f"<b>╚════════════════════════╝</b>\n\n"
    
    f"<b>ᴍᴇɴᴛɪᴏɴ ᴧʟʟ ɢʀᴏᴜᴘ ᴍᴇᴍʙᴇʀs ᴧᴛ ᴏɴᴄᴇ.</b>\n\n"
    
    f"<b>❖ ᴄᴏᴍᴍᴧɴᴅs ❖</b>\n\n"
    f"<b>➻ /tagall — ᴍᴇɴᴛɪᴏɴ ᴧʟʟ ᴍᴇᴍʙᴇʀs</b>\n"
    f"<b>➻ /tagall &lt;message&gt; — ᴡɪᴛʜ ᴄᴜsᴛᴏᴍ ᴍᴇssᴧɢᴇ</b>\n"
    f"<b>➻ /stop — sᴛᴏᴘ ᴛᴧɢɢɪɴɢ ɪᴍᴍᴇᴅɪᴧᴛᴇʟʏ</b>\n\n"
    
    f"<b>❖ ɴᴏᴛᴇs ❖</b>\n"
    f"<b>➻ ᴍᴇᴍʙᴇʀs ᴍᴇɴᴛɪᴏɴᴇᴅ ɪɴ ʙᴧᴛᴄʜᴇs ᴏғ 5</b>\n"
    f"<b>➻ ʙᴏᴛs ᴧɴᴅ ᴅᴇʟᴇᴛᴇᴅ ᴧᴄᴄᴏᴜɴᴛs sᴋɪᴘᴘᴇᴅ</b>\n"
    f"<b>➻ ᴏɴʟʏ ᴧᴅᴍɪɴs ᴄᴧɴ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴧɴᴅ</b>"
    f"</blockquote>"
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("⌯ 𝐁𝐚𝐜𝐤 ⌯", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=text, parse_mode=enums.ParseMode.HTML)
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
            text = (
    f"<blockquote expandable>"
    f"<b>╔══════════════════╗</b>\n"
    f"<b>👑 ᴘʀᴏᴍᴏᴛᴇ sʏsᴛᴇᴍ</b>\n"
    f"<b>╚══════════════════╝</b>\n\n"
    
    f"<b>ᴛʜʀᴇᴇ ʟᴇᴠᴇʟs ᴏғ ᴘʀᴏᴍᴏᴛɪᴏɴ:</b>\n\n"
    
    f"<b>➻ /promote &lt;user&gt; [title]</b>\n"
    f"<b>→ sᴛᴧɴᴅᴧʀᴅ ᴧᴅᴍɪɴ</b>\n\n"
    
    f"<b>➻ /mod &lt;user&gt; [title]</b>\n"
    f"<b>→ ᴍᴏᴅᴇʀᴧᴛᴏʀ ʀᴏʟᴇ</b>\n\n"
    
    f"<b>➻ /fullpromote &lt;user&gt; [title]</b>\n"
    f"<b>→ ғᴜʟʟ ᴧᴅᴍɪɴ (ᴧʟʟ ᴘᴏᴡᴇʀs)</b>\n\n"
    
    f"<b>➻ /demote &lt;user&gt;</b>\n"
    f"<b>→ ʀᴇᴍᴏᴠᴇ ᴧᴅᴍɪɴ ʀɪɢʜᴛs</b>\n\n"
    
    f"<b><i>ᴏɴʟʏ ᴧᴅᴍɪɴs ᴡɪᴛʜ ᴧᴅᴅ ᴧᴅᴍɪɴ ᴘᴇʀᴍɪssɪᴏɴ</i></b>\n"
    f"<b><i>ᴄᴧɴ ᴜsᴇ ᴛʜᴇsᴇ ᴄᴏᴍᴍᴧɴᴅs</i></b>"
    f"</blockquote>"
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("⌯ 𝐁𝐚𝐜𝐤 ⌯", callback_data="help")]])
            media = InputMediaPhoto(media=START_IMAGE, caption=text, parse_mode=enums.ParseMode.HTML)
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

    @app.on_callback_query(filters.regex("^blacklist_help$"))
    async def blacklist_help_callback(client, callback_query):
        from handlers.blacklist import BLACKLIST_HELP_TEXT
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("⌯ 𝐁𝐚𝐜𝐤 ⌯", callback_data="help")]])
        media = InputMediaPhoto(media=START_IMAGE, caption=BLACKLIST_HELP_TEXT, parse_mode=enums.ParseMode.HTML)
        await callback_query.message.edit_media(media=media, reply_markup=buttons)
        await callback_query.answer()

    @app.on_callback_query(filters.regex("^filters_help$"))
    async def filters_help_callback(client, callback_query):
        from handlers.filters import FILTERS_HELP_TEXT
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("⌯ 𝐁𝐚𝐜𝐤 ⌯", callback_data="help")]])
        media = InputMediaPhoto(media=START_IMAGE, caption=FILTERS_HELP_TEXT, parse_mode=enums.ParseMode.HTML)
        await callback_query.message.edit_media(media=media, reply_markup=buttons)
        await callback_query.answer()

    @app.on_callback_query(filters.regex("^joinrequest_help$"))
    async def joinrequest_help_callback(client, callback_query):
        from handlers.joinrequest import JOINREQUEST_HELP_TEXT
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("⌯ 𝐁𝐚𝐜𝐤 ⌯", callback_data="help")]])
        media = InputMediaPhoto(media=START_IMAGE, caption=JOINREQUEST_HELP_TEXT, parse_mode=enums.ParseMode.HTML)
        await callback_query.message.edit_media(media=media, reply_markup=buttons)
        await callback_query.answer()

