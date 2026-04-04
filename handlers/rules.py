# ============================================================
# Group Manager Bot
# Author: Mr. Stark
# ============================================================

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus
import db


async def is_power(client, chat_id: int, user_id: int) -> bool:
    member = await client.get_chat_member(chat_id, user_id)
    return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]


def register_rules_handler(app: Client):

    # ==========================================================
    # /setrules — Admin rules set kare (formatting preserve hoti hai)
    # ==========================================================

    @app.on_message(filters.group & filters.command("setrules"))
    async def setrules_cmd(client, message: Message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Only admin can set group rule. ")

        # /setrules ke baad ka poora text lao — newlines aur spaces sab preserve honge
        parts = message.text.split(maxsplit=1)
        if len(parts) < 2 or not parts[1].strip():
            return await message.reply_text(
                "⚙️ Usage:\n`/setrules <text>`\n\n"
                "Tip: The file will be saved as it is written. \n Newlines, spaces, etc. will be preserved. "
            )

        rules_text = parts[1]  # Exact text as-is — no strip, no modify
        await db.set_rules(message.chat.id, rules_text)
        await message.reply_text("✅ Rules is saved. `/rules` For see the Rule")


    # ==========================================================
    # /rules — Rules dikhao
    # ==========================================================

    @app.on_message(filters.group & filters.command("rules"))
    async def rules_cmd(client, message: Message):
        rules_text = await db.get_rules(message.chat.id)

        if not rules_text:
            return await message.reply_text(
                "📭  No rules have been set for this group.\n"
                "Admins can set this using `/setrules`."
            )

        # Exact formatting preserve karke dikhao
        header = (
            "╔══════════════════╗\n"
            "    📜 RULES\n"
            "╚══════════════════╝\n\n"
        )
        await message.reply_text(header + rules_text)


    # ==========================================================
    # /clearrules — Admin rules delete kare
    # ==========================================================

    @app.on_message(filters.group & filters.command("clearrules"))
    async def clearrules_cmd(client, message: Message):
        if not await is_power(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Sirf admin hi rules clear kar sakta hai.")

        existing = await db.get_rules(message.chat.id)
        if not existing:
            return await message.reply_text("⚠️ No rules have been set ")

        await db.clear_rules(message.chat.id)
        await message.reply_text("🗑️ rule deleted ")
