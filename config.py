# ============================================================
#Group Manager Bot
# Author: LearningBotsOfficial (https://github.com/LearningBotsOfficial) 
# Support: https://t.me/LearningBotsCommunity
# Channel: https://t.me/learning_bots
# YouTube: https://youtube.com/@learning_bots
# License: Open-source (keep credits, no resale)
# ============================================================

import os
from dotenv import load_dotenv

load_dotenv()

# Required configurations
API_ID = int(os.getenv("API_ID", 38881334))
API_HASH = os.getenv("API_HASH", "b28ea0d569fb81f8053484a227514135")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
MONGO_URI = os.getenv("MONGO_URI", "")
DB_NAME = os.getenv("DB_NAME", "Cluster0")

OWNER_ID = int(os.getenv("OWNER_ID", 8275132868))
BOT_USERNAME = os.getenv("BOT_USERNAME", "EdithHelpsBot")

SUPPORT_GROUP = os.getenv("SUPPORT_GROUP", "https://t.me/CarelessxWorld")
UPDATE_CHANNEL = os.getenv("UPDATE_CHANNEL", "https://t.me/+wQonHdyvZh5mZWM1")
START_IMAGE = os.getenv("START_IMAGE", "https://files.catbox.moe/676gur.jpg")
