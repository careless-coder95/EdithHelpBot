# ============================================================
# Group Manager Bot
# Author: Mr. Stark
# ============================================================

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatMemberStatus
import db


async def is_power(client, chat_id: int, user_id: int) -> bool:
    member = await client.get_chat_member(chat_id, user_id)
    return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]


def register_notes_handler(app: Client):

    # ==========================================================
    # /setnote — Admin note save kare
    # ==========================================================

    @app.on_message(filters.group & filters.command("setnote"))
    async def setnote_cmd(client, message: Message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Sirf admin hi note set kar sakta hai.")

        parts = message.text.split(maxsplit=2)
        if len(parts) < 3:
            return await message.reply_text(
                "⚙️ Usage: `/setnote <name> <content>`\n\n"
                "Example: `/setnote rules Yahan koi spam nahi karega!`"
            )

        name = parts[1].lower()
        content = parts[2]

        await db.set_note(message.chat.id, name, content)
        await message.reply_text(f"✅ Note `{name}` save ho gaya!\n\nDekho: `#{name}`")


    # ==========================================================
    # /delnote — Admin note delete kare
    # ==========================================================

    @app.on_message(filters.group & filters.command("delnote"))
    async def delnote_cmd(client, message: Message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Sirf admin hi note delete kar sakta hai.")

        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            return await message.reply_text("⚙️ Usage: `/delnote <name>`")

        name = parts[1].lower()
        deleted = await db.delete_note(message.chat.id, name)

        if deleted:
            await message.reply_text(f"🗑️ Note `{name}` delete ho gaya.")
        else:
            await message.reply_text(f"⚠️ `{name}` naam ka koi note nahi mila.")


    # ==========================================================
    # /notes — Sabke notes ki list
    # ==========================================================

    @app.on_message(filters.group & filters.command("notes"))
    async def notes_list_cmd(client, message: Message):
        names = await db.get_all_notes(message.chat.id)

        if not names:
            return await message.reply_text("📭 Is group mein abhi koi note nahi hai.")

        # Har note ke liye ek button banao jo bot ke private chat mein open ho
        bot_username = (await client.get_me()).username
        buttons = []
        for name in names:
            # Deep link: t.me/BotUsername?start=note_chatid_notename
            deep_link = f"https://t.me/{bot_username}?start=note_{message.chat.id}_{name}"
            buttons.append([InlineKeyboardButton(f"📝 #{name}", url=deep_link)])

        text = f"╔════════════════════════╗\n   📝 NOTES — {message.chat.title}\n╚════════════════════════╝\n\nNeeche se note open karo:"

        await message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))


    # ==========================================================
    # #note_name — Group mein hashtag se note dekho
    # ==========================================================

    @app.on_message(filters.group & filters.regex(r"^#(\w+)"))
    async def hashtag_note(client, message: Message):
        match = message.matches[0]
        name = match.group(1).lower()

        content = await db.get_note(message.chat.id, name)
        if not content:
            return  # Koi response nahi agar note nahi mila

        bot_username = (await client.get_me()).username
        deep_link = f"https://t.me/{bot_username}?start=note_{message.chat.id}_{name}"

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"📖 #{name} Dekho", url=deep_link)]
        ])

        await message.reply_text(
            f"📝 Note `#{name}` available hai!\nPrivate mein poora padhne ke liye neeche click karo:",
            reply_markup=buttons
        )


    # ==========================================================
    # Private mein note open — deep link se
    # ==========================================================

    @app.on_message(filters.private & filters.command("start"))
    async def note_deep_link(client, message: Message):
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            return  # Normal start handle hoga start.py mein

        payload = args[1]

        # Format: note_chatid_notename
        if not payload.startswith("note_"):
            return  # Normal /start handle karo

        try:
            _, chat_id_str, name = payload.split("_", 2)
            chat_id = int(chat_id_str)
        except ValueError:
            return await message.reply_text("❌ Invalid link.")

        content = await db.get_note(chat_id, name)
        if not content:
            return await message.reply_text(f"⚠️ Note `#{name}` nahi mila ya delete ho gaya.")

        await message.reply_text(
            f"╔════════════════════════╗\n"
            f"   📝 Note: #{name}\n"
            f"╚════════════════════════╝\n\n"
            f"{content}"
        )
