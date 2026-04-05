# ============================================================
#Group Manager Bot
#AUTHOR : MISTER STARK 
# ============================================================

from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
import logging

# 🔐 Import security
from security import verify_integrity, get_runtime_key

logging.basicConfig(level=logging.INFO)

verify_integrity()

RUNTIME_KEY = get_runtime_key()

app = Client(
    "group_manager_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

from handlers import register_all_handlers
register_all_handlers(app)

print("✅ Bot is starting securely...")

app.run()
