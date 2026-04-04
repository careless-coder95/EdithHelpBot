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
            f"\n"
            f"   ✨ <b>Hello {user}!</b> ✨\n\n"
            f"👋 I am <b>Nomad 🤖</b>\n\n"
            f"<b>Highlights:</b>\n"
            f"─────────────────────────────\n"
            f"- Smart Anti-Spam &amp; Link Shield\n"
            f"- Adaptive Lock System (URLs, Media, Text &amp; more)\n"
            f"- BioLink Protection System\n"
            f"- Notes &amp; Rules Management\n"
            f"- Modular &amp; Scalable Protection\n"
            f"- Sleek UI with Inline Controls\n\n"
            f"» <b>More New Features coming soon ...</b>\n"
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
            "╔══════════════════╗\n"
            "    ⚙ <b>Welcome System</b>\n"
            "╚══════════════════╝\n\n"
            "<b>Commands to Manage Welcome Messages:</b>\n\n"
            "- <b>/setwelcome</b> &lt;text&gt; : Set a custom welcome message\n"
            "- <b>/welcome on</b>        : Enable welcome messages\n"
            "- <b>/welcome off</b>       : Disable welcome messages\n\n"
            "<b>Supported Placeholders:</b>\n"
            "- <code>{username}</code>   : Telegram username\n"
            "- <code>{first_name}</code> : User's first name\n"
            "- <code>{mention}</code>    : Mention user in message\n"
            "- <code>{title}</code>      : Group title\n\n"
            "<b>Example:</b>\n"
            " /setwelcome Hello {first_name}! Welcome to {title}!\n"
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
            "     ⚙ <b>Locks System</b>\n"
            "╚══════════════════╝\n\n"
            "<b>Commands to Manage Locks:</b>\n\n"
            "- <b>/lock</b> &lt;type&gt;    : Enable a lock\n"
            "- <b>/unlock</b> &lt;type&gt;  : Disable a lock\n"
            "- <b>/locks</b>          : Show active locks\n\n"
            "<b>Available Lock Types:</b>\n"
            "- <code>url</code>      : Block links/URLs\n"
            "- <code>sticker</code>  : Block stickers\n"
            "- <code>media</code>    : Block photos/videos/docs\n"
            "- <code>username</code> : Block @mention messages\n"
            "- <code>forward</code>  : Block forwarded messages\n"
            "- <code>text</code>     : Block ALL text messages\n"
            "- <code>edit</code>     : Delete edited messages\n\n"
            "<b>Example:</b>\n"
            " /lock text   → Koi bhi text msg nahi kar payega\n"
            " /lock edit   → Koi edit kare to message delete hoga\n"
            " /unlock url  → Links phir allow honge\n"
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
                "      ⚙️ <b>Moderation</b>\n"
                "╚══════════════════╝\n\n"
                "<b>Manage your group easily:</b>\n\n"
                "¤ <b>/kick</b> &lt;user&gt;       — Remove a user\n"
                "¤ <b>/ban</b> &lt;user&gt;        — Ban permanently\n"
                "¤ <b>/unban</b> &lt;user&gt;      — Lift ban\n"
                "¤ <b>/mute</b> &lt;user&gt;       — Disable messages\n"
                "¤ <b>/unmute</b> &lt;user&gt;     — Allow messages again\n"
                "¤ <b>/warn</b> &lt;user&gt;       — Add warning (3 = mute)\n"
                "¤ <b>/warns</b> &lt;user&gt;      — View warnings\n"
                "¤ <b>/resetwarns</b> &lt;user&gt; — Clear all warnings\n"
                "¤ <b>/promote</b> &lt;user&gt;    — Make admin\n"
                "¤ <b>/demote</b> &lt;user&gt;     — Remove from admin\n\n"
                "💡 <b>Usage:</b>\n"
                "Reply to a user or type /ban @username\n"
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
                "╔══════════════════╗\n"
                "    🔗 <b>BioLink Protection</b>\n"
                "╚══════════════════╝\n\n"
                "Un users ko rokta hai jinke bio me\n"
                "koi bhi link hota hai.\n\n"
                "<b>Commands:</b>\n\n"
                "¤ <b>/biolink on</b>  — Protection ON karo\n"
                "¤ <b>/biolink off</b> — Protection OFF karo\n\n"
                "<b>Kaise kaam karta hai:</b>\n"
                "- Jab user message karta hai, bot\n"
                "  uski bio check karta hai.\n"
                "- Bio me link mila → message delete.\n"
                "- User ko samjhaya jaata hai.\n\n"
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
            print(f"Error in biolink_callback: {e}")
            await callback_query.answer("❌ Something went wrong.", show_alert=True)


    # ==========================================================
    # Notes help callback
    # ==========================================================
    @app.on_callback_query(filters.regex("^notes_help$"))
    async def notes_help_callback(client, callback_query):
        try:
            text = (
                "╔════════════════════════╗\n"
                "   📝 <b>NOTES</b>\n"
                "╚════════════════════════╝\n\n"
                "👮 <b>Admin Commands:</b>\n"
                "• <b>/setnote</b> &lt;n&gt; &lt;content&gt;\n"
                "  → Note save karo\n\n"
                "• <b>/delnote</b> &lt;n&gt;\n"
                "  → Note delete karo\n\n"
                "👥 <b>User Commands:</b>\n"
                "• <b>/notes</b>\n"
                "  → Sabke notes ki list dekho\n"
                "  (Har note ka private link milega)\n\n"
                "• <b>#note_name</b>\n"
                "  → Group me type karo, bot\n"
                "    private link bhejega\n\n"
                "💡 <b>Example:</b>\n"
                " /setnote welcome Yahan spam mat karo!\n"
                " #welcome  → Note ka link milega\n"
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
