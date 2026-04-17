# ============================================================
# Group Manager Bot — Welcome System (Advanced)
# Author: Mr. Stark
# ============================================================

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ChatMemberStatus, ChatMemberUpdated
from datetime import datetime
import re
import logging
import db

logger = logging.getLogger(__name__)

# ==========================================================
# Markdown Help Text
# ==========================================================

MARKDOWN_HELP_TEXT = """
╔══════════════════════════╗
   📝 WELCOME FORMATTING GUIDE
╚══════════════════════════╝

**Supported Fillings:**

• `{GROUPNAME}` — Group name
• `{NAME}` — Full name
• `{FIRSTNAME}` — First name
• `{SURNAME}` — Last name (empty if none)
• `{USERNAME}` — @username (empty if none)
• `{ID}` — User ID
• `{TIME}` — Current time
• `{DATE}` — Current date
• `{WEEKDAY}` — Current weekday

─────────────────────────

**Text Formatting:**

• `**Bold**` → **Bold**
• `__italic__` → __italic__
• `~~strike~~` → ~~strike~~
• `--underline--` → underline
• `` `code` `` → `code`
• `||spoiler||` → ||spoiler||
• `[text](url)` → hyperlink
• `> quote` → blockquote

─────────────────────────

**Button Formatting:**

```
Your welcome text here
[Button Text, https://link.com]
```

**Example:**
```
Welcome {FIRSTNAME} to {GROUPNAME}!
[Join Channel, https://t.me/yourchannel]
```
"""

# ==========================================================
# Formatting helpers
# ==========================================================

def parse_underline(text: str) -> str:
    """--text-- → <u>text</u>"""
    return re.sub(r"--(.+?)--", r"<u>\1</u>", text)


def fill_placeholders(text: str, user, chat) -> str:
    now = datetime.now()
    surname = user.last_name or ""
    username = f"@{user.username}" if user.username else ""

    replacements = {
        "{GROUPNAME}": chat.title or "",
        "{NAME}": user.first_name + (" " + surname if surname else ""),
        "{FIRSTNAME}": user.first_name or "",
        "{SURNAME}": surname,
        "{USERNAME}": username,
        "{ID}": str(user.id),
        "{TIME}": now.strftime("%I:%M %p"),
        "{DATE}": now.strftime("%d %B %Y"),
        "{WEEKDAY}": now.strftime("%A"),
    }

    for key, value in replacements.items():
        text = text.replace(key, value)
    return text


def parse_buttons(text: str):
    """
    Parse [Button Text, https://link.com] from text.
    Returns (clean_text, buttons_list)
    """
    button_pattern = re.compile(r"\[(.+?),\s*(https?://\S+)\]")
    buttons = []

    for match in button_pattern.finditer(text):
        btn_text = match.group(1).strip()
        btn_url = match.group(2).strip()
        buttons.append(InlineKeyboardButton(btn_text, url=btn_url))

    clean_text = button_pattern.sub("", text).strip()
    return clean_text, buttons


def build_keyboard(buttons: list) -> InlineKeyboardMarkup | None:
    if not buttons:
        return None
    # 2 buttons per row
    rows = []
    for i in range(0, len(buttons), 2):
        rows.append(buttons[i:i+2])
    return InlineKeyboardMarkup(rows)


# ==========================================================
# Help Text
# ==========================================================

WELCOME_HELP_TEXT = """
╔══════════════════╗
   👋 WELCOME SYSTEM
╚══════════════════╝

Commands:

• /welcome on/off
  → Enable or disable welcome

• /setwelcome <text>
  → Set custom welcome message

• /resetwelcome
  → Reset to default welcome

• /markdown
  → View formatting guide

Supported Placeholders:
{FIRSTNAME} {SURNAME} {NAME}
{USERNAME} {ID} {GROUPNAME}
{TIME} {DATE} {WEEKDAY}

Button Format:
[Button Text, https://link.com]

👮 Only admins can configure.
"""


def register_welcome_handler(app: Client):

    # ==========================================================
    # New member — trigger welcome
    # ==========================================================

    @app.on_chat_member_updated()
    async def member_update(client: Client, cmu: ChatMemberUpdated):
        if not cmu.new_chat_member:
            return

        user = cmu.new_chat_member.user
        new_status = cmu.new_chat_member.status

        if new_status != ChatMemberStatus.MEMBER:
            return

        status = await db.get_welcome_status(cmu.chat.id)
        if not status:
            return

        template = await db.get_welcome_message(cmu.chat.id)
        if not template:
            template = "👋 Welcome **{FIRSTNAME}** to **{GROUPNAME}**!"

        try:
            filled = fill_placeholders(template, user, cmu.chat)
            filled = parse_underline(filled)
            clean_text, buttons = parse_buttons(filled)
            keyboard = build_keyboard(buttons)

            await client.send_message(
                cmu.chat.id,
                clean_text,
                reply_markup=keyboard,
                parse_mode=None  # Pyrogram auto-detects markdown/html
            )
        except Exception as e:
            logger.error(f"Welcome send error: {e}")


    # ==========================================================
    # /welcome on/off
    # ==========================================================

    @app.on_message(filters.group & filters.command("welcome"))
    async def welcome_toggle(client, message: Message):
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return await message.reply_text("❌ Only admins can use this command.")

        parts = message.text.split(maxsplit=1)
        if len(parts) < 2 or parts[1].lower() not in ["on", "off"]:
            status = await db.get_welcome_status(message.chat.id)
            return await message.reply_text(
                f"⚙️ Usage: `/welcome on` or `/welcome off`\n\n"
                f"📊 Current: {'🟢 ON' if status else '🔴 OFF'}"
            )

        status = parts[1].lower() == "on"
        await db.set_welcome_status(message.chat.id, status)
        await message.reply_text(
            "✅ **Welcome messages ON!**" if status else "⚠️ **Welcome messages OFF!**"
        )


    # ==========================================================
    # /setwelcome
    # ==========================================================

    @app.on_message(filters.group & filters.command("setwelcome"))
    async def set_welcome(client, message: Message):
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return await message.reply_text("❌ Only admins can use this command.")

        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            return await message.reply_text(
                "⚙️ Usage: `/setwelcome <text>`\n\n"
                "Use /markdown to see all formatting options."
            )

        await db.set_welcome_message(message.chat.id, parts[1])
        await message.reply_text(
            "✅ **Welcome message saved!**\n\n"
            "Use /markdown to see formatting options."
        )


    # ==========================================================
    # /resetwelcome
    # ==========================================================

    @app.on_message(filters.group & filters.command("resetwelcome"))
    async def reset_welcome(client, message: Message):
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return await message.reply_text("❌ Only admins can use this command.")

        await db.set_welcome_message(message.chat.id, "")
        await message.reply_text("✅ Welcome message reset to default.")


    # ==========================================================
    # /markdown — formatting guide
    # ==========================================================

    @app.on_message(filters.command("markdown"))
    async def markdown_cmd(client, message: Message):
        await message.reply_text(MARKDOWN_HELP_TEXT)
