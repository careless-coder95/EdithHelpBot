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
            f"\n   ✨ Hello {user}! ✨\n\n"
            f"👋 I am Nomad 🤖\n\n"
            f"Highlights:\n"
            f"─────────────────────────────\n"
            f"- Smart Anti-Spam &amp; Link Shield\n"
            f"- Adaptive Lock System (URLs, Media, Text &amp; more)\n"
            f"- BioLink Protection System\n"
            f"- Notes &amp; Rules Management\n"
            f"- Modular &amp; Scalable Protection\n"
            f"- Sleek UI with Inline Controls\n\n"
            f"» More New Features coming soon ..."
        )
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("⚒️ Add to Group ⚒️", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
            [
                InlineKeyboardButton("⌂ Support ⌂", url=SUPPORT_GROUP),
                InlineKeyboardButton("⌂ Update ⌂", url=UPDATE_CHANNEL),
            ],
            [
                InlineKeyboardButton("※ ŎŴɳēŔ ※", url=f"tg://user?id={OWNER_ID}"),
                InlineKeyboardButton("Repo", url="https://github.com/careless-coder95/EdithHelpBot"),
            ],
            [InlineKeyboardButton("📚 Help Commands 📚", callback_data="help")]
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
                f"   📝 Note: <b>#{name}</b>\n"
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
        ("⌂ Greetings", "greetings"),
        ("🔒 Locks", "locks"),
        ("👮 Moderation", "moderation"),
        ("🔗 BioLink", "biolink"),
        ("📝 Notes", "notes_help"),
        ("📜 Rules", "rules_help"),
        ("🤬 Abuse", "abuse_help"),
        ("📢 F-Sub", "fsub_help"),
        ("📢 Echo", "echo_help"),
        ("📞 Phone", "phone_help"),
        ("📄 Long Limit", "longmsg_help"),
        ("# Hashtag", "hashtag_help"),
        ("⚙️ Utility", "utility_help"),
        ("🗑️ Cmd Deleter", "cmd_help"),
        ("🎬 Media Delete", "mediadelete_help"),
        ("🧹 Cleaner", "cleaner_help"),
        ("🧟 Zombie", "zombie_help"),
        ("📢 Tag All", "tagall_help"),
        ("👑 Promote", "promote_help"),
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
            nav.append(InlineKeyboardButton("◀ Prev", callback_data=f"helppage_{page - 1}"))
        else:
            nav.append(InlineKeyboardButton("◀", callback_data="noop"))

        nav.append(InlineKeyboardButton("🏠 Back", callback_data="back_to_start"))

        if page < TOTAL_PAGES - 1:
            nav.append(InlineKeyboardButton("Next ▶", callback_data=f"helppage_{page + 1}"))
        else:
            nav.append(InlineKeyboardButton("▶", callback_data="noop"))

        rows.append(nav)

        text = (
            f"╔══════════════════╗\n"
            f"     Help Menu\n"
            f"╚══════════════════╝\n\n"
            f"Page <b>{page + 1}</b> of <b>{TOTAL_PAGES}</b>\n"
            f"Choose a category:"
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
            "╔══════════════════╗\n"
            "    ⚙ Welcome System\n"
            "╚══════════════════╝\n\n"
            "<b>Commands:</b>\n\n"
            "• /setwelcome &lt;text&gt; — Set custom welcome\n"
            "• /welcome on — Enable welcome\n"
            "• /welcome off — Disable welcome\n\n"
            "<b>Placeholders:</b>\n"
            "<code>{username}</code>   — Telegram username\n"
            "<code>{first_name}</code> — User's first name\n"
            "<code>{mention}</code>    — Mention user\n"
            "<code>{title}</code>      — Group title\n\n"
            "<b>Example:</b>\n"
            "<code>/setwelcome Hello {first_name}! Welcome to {title}!</code>"
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
            "╔══════════════════╗\n"
            "     ⚙ Locks System\n"
            "╚══════════════════╝\n\n"
            "<b>Commands:</b>\n\n"
            "• /lock &lt;type&gt;  — Enable a lock\n"
            "• /unlock &lt;type&gt; — Disable a lock\n"
            "• /locks          — Show active locks\n"
            "• /lockall        — Lock everything 🔐\n"
            "• /unlockall      — Unlock everything 🔓\n\n"
            "<b>Available Types:</b>\n"
            "<code>url</code> • <code>text</code> • <code>sticker</code> • <code>media</code>\n"
            "<code>username</code> • <code>forward</code> • <code>edit</code>"
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
                "╔══════════════════╗\n"
                "      ⚙️ Moderation\n"
                "╚══════════════════╝\n\n"
                "• /kick &lt;user&gt;         — Remove a user\n"
                "• /ban &lt;user&gt;          — Ban permanently\n"
                "• /unban &lt;user&gt;        — Lift ban\n"
                "• /mute &lt;user&gt;         — Disable messages\n"
                "• /unmute &lt;user&gt;       — Allow messages again\n"
                "• /tmute &lt;user&gt; &lt;time&gt; — Temp mute (1m–24h)\n"
                "• /tban &lt;user&gt; &lt;time&gt;  — Temp ban (1m–24h)\n"
                "• /warn &lt;user&gt;         — Warning (3 = mute)\n"
                "• /warns &lt;user&gt;        — View warnings\n"
                "• /resetwarns &lt;user&gt;   — Clear warnings\n\n"
                "<i>Reply to a user or type /ban @username</i>"
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
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
                "╔══════════════════╗\n"
                "    🔗 BioLink Protection\n"
                "╚══════════════════╝\n\n"
                "Blocks users who have links in their bio.\n\n"
                "<b>Commands:</b>\n\n"
                "• /biolink on  — Protection ON ✅\n"
                "• /biolink off — Protection OFF ❌\n\n"
                "<b>Notes:</b>\n"
                "- Bio link detected → message deleted.\n"
                "- Admins are not affected.\n"
                "- Bot needs Delete Messages permission."
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
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
                "╔════════════════════════╗\n"
                "   📝 NOTES\n"
                "╚════════════════════════╝\n\n"
                "<b>👮 Admin Commands:</b>\n"
                "• /setnote &lt;name&gt; &lt;content&gt;\n"
                "• /delnote &lt;name&gt;\n\n"
                "<b>👥 User Commands:</b>\n"
                "• /notes — List all notes\n"
                "• #note_name — Get private link\n\n"
                "<i>Each note opens in private chat via link.</i>"
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
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
                "╔══════════════════╗\n"
                "   📜 RULES\n"
                "╚══════════════════╝\n\n"
                "<b>Commands:</b>\n\n"
                "• /setrules &lt;text&gt; — Set group rules\n"
                "• /rules           — Show current rules\n"
                "• /clearrules      — Remove all rules\n\n"
                "🌟 Formatting is preserved exactly as typed."
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
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
                "╔══════════════════╗\n"
                "   🤬 Abuse Detection\n"
                "╚══════════════════╝\n\n"
                "Abusive messages are automatically deleted.\n\n"
                "<b>Commands:</b>\n\n"
                "• /noabuse on  — Enable ✅\n"
                "• /noabuse off — Disable ❌\n\n"
                "<b>Notes:</b>\n"
                "- Message deleted instantly.\n"
                "- 5 second warning sent.\n"
                "- Admins not affected."
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
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
                "╔══════════════════╗\n"
                "   🔗 FORCE-SUBSCRIBE\n"
                "╚══════════════════╝\n\n"
                "Users who haven't joined required\n"
                "channels cannot send messages.\n\n"
                "<b>Commands:</b>\n\n"
                "• /addfsub @channel    — Add channel\n"
                "• /removefsub @channel — Remove channel\n"
                "• /fsublist            — List channels\n\n"
                "<i>Bot must be admin in the channel.</i>"
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
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
                "╔══════════════════╗\n"
                "   📄 LONG MESSAGE\n"
                "╚══════════════════╝\n\n"
                "Long messages are uploaded to Telegraph\n"
                "and sent as a link automatically.\n\n"
                "<b>Commands:</b>\n\n"
                "• /echo &lt;text&gt; — Echo text\n"
                "• /setlongmode off — No action\n"
                "• /setlongmode manual — Delete + warn\n"
                "• /setlongmode automatic — Delete + link ✅\n"
                "• /setlonglimit &lt;200–4000&gt; — Set limit\n\n"
                "<i>Default limit: 800 characters</i>"
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
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
                "╔══════════════════╗\n"
                "   📞 PHONE PROTECTION\n"
                "╚══════════════════╝\n\n"
                "Phone numbers in messages are\n"
                "automatically deleted.\n\n"
                "<b>Commands:</b>\n\n"
                "• /nophone on  — Block ✅\n"
                "• /nophone off — Allow ❌\n\n"
                "<b>Detection:</b>\n"
                "• +91 9876543210\n"
                "• +1-234-567-8900\n"
                "• 919876543210"
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
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
                "╔══════════════════╗\n"
                "   📄 LONG MESSAGE\n"
                "╚══════════════════╝\n\n"
                "<b>Commands:</b>\n\n"
                "• /setlongmode off — No action\n"
                "• /setlongmode manual — Delete + warn\n"
                "• /setlongmode automatic — Delete + link\n"
                "• /setlonglimit &lt;200–4000&gt; — Character limit\n\n"
                "<i>Default: automatic mode, 800 chars</i>"
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
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
                "╔══════════════════╗\n"
                "   # HASHTAG FILTER\n"
                "╚══════════════════╝\n\n"
                "Hashtag messages are automatically deleted.\n\n"
                "<b>Commands:</b>\n\n"
                "• /nohashtags on  — Block ✅\n"
                "• /nohashtags off — Allow ❌\n\n"
                "<b>Detection:</b>\n"
                "• #join, #promotion, #trending\n"
                "• Any word starting with #"
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
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
                "╔══════════════════╗\n"
                "   ⚙️ UTILITY\n"
                "╚══════════════════╝\n\n"
                "• /chatinfo — Group details &amp; member count\n"
                "• /id       — Your ID or replied user's ID\n"
                "• /pin      — Pin a replied message\n"
                "• /unpin    — Unpin message or all pins\n"
                "• /purge    — Bulk delete messages\n"
                "• /del      — Delete a replied message\n"
                "• /report   — Report a user to admins\n\n"
                "<i>pin, purge, del — admin only.</i>"
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
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
                "╔══════════════════╗\n"
                "   🗑️ CMD DELETER\n"
                "╚══════════════════╝\n\n"
                "Commands starting with <code>/</code> <code>!</code> <code>.</code>\n"
                "are automatically deleted.\n\n"
                "<b>Commands:</b>\n\n"
                "• /cmd on  — Auto delete ON ✅\n"
                "• /cmd off — Auto delete OFF ❌\n\n"
                "<i>Admins are not affected.</i>"
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
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
                "╔══════════════════╗\n"
                "   🎬 MEDIA AUTO-DELETE\n"
                "╚══════════════════╝\n\n"
                "Media messages are automatically deleted\n"
                "after a configured delay.\n\n"
                "<b>Commands:</b>\n\n"
                "• /mediadelete on  — Enable ✅\n"
                "• /mediadelete off — Disable ❌\n"
                "• /setmediadelay &lt;time&gt; — Set delay\n\n"
                "<b>Applies to:</b>\n"
                "Photos, Videos, Stickers, GIFs,\n"
                "Animations, Locations, Polls\n\n"
                "<i>Range: 1m to 24h — Default: 5m</i>"
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
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
                "╔══════════════════╗\n"
                "   🧹 MESSAGE CLEANER\n"
                "╚══════════════════╝\n\n"
                "All regular user messages are deleted\n"
                "automatically after a set delay.\n\n"
                "<b>Commands:</b>\n\n"
                "• /cleaner on  — Enable ✅\n"
                "• /cleaner off — Disable ❌\n"
                "• /setcleandelay &lt;time&gt; — Set delay\n"
                "• /cleanstatus — Show settings\n\n"
                "<b>Notes:</b>\n"
                "- Admin messages are never deleted.\n"
                "- Range: 1m to 24h — Default: 5m"
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
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
                "╔════════════════════╗\n"
                "   ⚠️ ZOMBIE REMOVER\n"
                "╚════════════════════╝\n\n"
                "Scans and removes all deleted Telegram\n"
                "accounts from the group.\n\n"
                "<b>Commands:</b>\n\n"
                "• /zombie — Scan &amp; remove deleted accounts\n\n"
                "<b>Notes:</b>\n"
                "- Bot must be admin with ban permission.\n"
                "- Only admins can use this command."
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
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
                "╔════════════════════════╗\n"
                "   📢 TAG ALL\n"
                "╚════════════════════════╝\n\n"
                "Mention all group members at once.\n\n"
                "<b>Commands:</b>\n\n"
                "• /tagall — Mention all members\n"
                "• /tagall &lt;message&gt; — With custom message\n"
                "• /stop — Stop tagging immediately\n\n"
                "<b>Notes:</b>\n"
                "- Members mentioned in batches of 5.\n"
                "- Bots and deleted accounts skipped.\n"
                "- Only admins can use this command."
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
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
                "╔══════════════════╗\n"
                "   👑 PROMOTE SYSTEM\n"
                "╚══════════════════╝\n\n"
                "Three levels of promotion:\n\n"
                "• /promote &lt;user&gt; [title]\n"
                "  → Standard admin\n\n"
                "• /mod &lt;user&gt; [title]\n"
                "  → Moderator role\n\n"
                "• /fullpromote &lt;user&gt; [title]\n"
                "  → Full admin (all powers)\n\n"
                "• /demote &lt;user&gt;\n"
                "  → Remove admin rights\n\n"
                "<i>Only admins with Add Admin permission\n"
                "can use these commands.</i>"
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help")]])
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
