# ============================================================
# Group Manager Bot
# Author: Mr. Stark
# ============================================================

import motor.motor_asyncio
from config import MONGO_URI, DB_NAME
import logging

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

logging.info("✅ MongoDB initialized")

# ==========================================================
# 🟢 Welcome
# ==========================================================

async def set_welcome_message(chat_id, text: str):
    await db.welcome.update_one({"chat_id": chat_id}, {"$set": {"message": text}}, upsert=True)

async def get_welcome_message(chat_id):
    data = await db.welcome.find_one({"chat_id": chat_id})
    return data.get("message") if data else None

async def set_welcome_status(chat_id, status: bool):
    await db.welcome.update_one({"chat_id": chat_id}, {"$set": {"enabled": status}}, upsert=True)

async def get_welcome_status(chat_id) -> bool:
    data = await db.welcome.find_one({"chat_id": chat_id})
    return bool(data.get("enabled", True)) if data else True


# ==========================================================
# 🔒 Lock
# ==========================================================

async def set_lock(chat_id, lock_type, status: bool):
    await db.locks.update_one({"chat_id": chat_id}, {"$set": {f"locks.{lock_type}": status}}, upsert=True)

async def get_locks(chat_id):
    data = await db.locks.find_one({"chat_id": chat_id})
    return data.get("locks", {}) if data else {}


# ==========================================================
# ⚠️ Warn
# ==========================================================

async def add_warn(chat_id: int, user_id: int) -> int:
    data = await db.warns.find_one({"chat_id": chat_id, "user_id": user_id})
    warns = data.get("count", 0) + 1 if data else 1
    await db.warns.update_one({"chat_id": chat_id, "user_id": user_id}, {"$set": {"count": warns}}, upsert=True)
    return warns

async def get_warns(chat_id: int, user_id: int) -> int:
    data = await db.warns.find_one({"chat_id": chat_id, "user_id": user_id})
    return data.get("count", 0) if data else 0

async def reset_warns(chat_id: int, user_id: int):
    await db.warns.update_one({"chat_id": chat_id, "user_id": user_id}, {"$set": {"count": 0}}, upsert=True)


# ==========================================================
# 🧹 Cleanup
# ==========================================================

async def clear_group_data(chat_id: int):
    await db.welcome.delete_one({"chat_id": chat_id})
    await db.locks.delete_one({"chat_id": chat_id})
    await db.warns.delete_many({"chat_id": chat_id})


# ==========================================================
# 👤 User
# ==========================================================

async def add_user(user_id, first_name):
    await db.users.update_one({"user_id": user_id}, {"$set": {"first_name": first_name}}, upsert=True)

async def get_all_users():
    users = []
    async for document in db.users.find({}, {"_id": 0, "user_id": 1}):
        if "user_id" in document:
            users.append(document["user_id"])
    return users


# ==========================================================
# 🔗 BioLink
# ==========================================================

async def set_biolink_status(chat_id: int, status: bool):
    await db.biolink.update_one({"chat_id": chat_id}, {"$set": {"enabled": status}}, upsert=True)

async def get_biolink_status(chat_id: int) -> bool:
    data = await db.biolink.find_one({"chat_id": chat_id})
    return bool(data.get("enabled", False)) if data else False


# ==========================================================
# 📝 Notes
# ==========================================================

async def set_note(chat_id: int, name: str, content: str):
    await db.notes.update_one(
        {"chat_id": chat_id, "name": name.lower()},
        {"$set": {"content": content}},
        upsert=True
    )

async def get_note(chat_id: int, name: str):
    data = await db.notes.find_one({"chat_id": chat_id, "name": name.lower()})
    return data.get("content") if data else None

async def delete_note(chat_id: int, name: str) -> bool:
    result = await db.notes.delete_one({"chat_id": chat_id, "name": name.lower()})
    return result.deleted_count > 0

async def get_all_notes(chat_id: int) -> list:
    names = []
    async for doc in db.notes.find({"chat_id": chat_id}, {"name": 1}):
        names.append(doc["name"])
    return sorted(names)


# ==========================================================
# 📜 Rules
# ==========================================================

async def set_rules(chat_id: int, text: str):
    await db.rules.update_one({"chat_id": chat_id}, {"$set": {"text": text}}, upsert=True)

async def get_rules(chat_id: int):
    data = await db.rules.find_one({"chat_id": chat_id})
    return data.get("text") if data else None

async def clear_rules(chat_id: int):
    await db.rules.delete_one({"chat_id": chat_id})


# ==========================================================
# 🤬 Abuse Detection
# ==========================================================

async def set_abuse_status(chat_id: int, status: bool):
    await db.abuse.update_one({"chat_id": chat_id}, {"$set": {"enabled": status}}, upsert=True)

async def get_abuse_status(chat_id: int) -> bool:
    data = await db.abuse.find_one({"chat_id": chat_id})
    return bool(data.get("enabled", False)) if data else False


# ==========================================================
# 📢 Force Subscribe
# ==========================================================

async def add_fsub_channel(chat_id: int, channel_id: str):
    await db.fsub.update_one(
        {"chat_id": chat_id},
        {"$addToSet": {"channels": channel_id}},
        upsert=True
    )

async def remove_fsub_channel(chat_id: int, channel_id: str) -> bool:
    result = await db.fsub.update_one(
        {"chat_id": chat_id},
        {"$pull": {"channels": channel_id}}
    )
    return result.modified_count > 0

async def get_fsub_channels(chat_id: int) -> list:
    data = await db.fsub.find_one({"chat_id": chat_id})
    return data.get("channels", []) if data else []




# ==========================================================
# 📃 LONG MESSAGE 
# ==========================================================

async def set_longmode(chat_id, mode):
    await db.longmsg.update_one({"chat_id": chat_id}, {"$set": {"mode": mode}}, upsert=True)
async def get_longmode(chat_id):
    data = await db.longmsg.find_one({"chat_id": chat_id})
    return data.get("mode", "automatic") if data else "automatic"
async def set_longlimit(chat_id, limit):
    await db.longmsg.update_one({"chat_id": chat_id}, {"$set": {"limit": limit}}, upsert=True)
async def get_longlimit(chat_id):
    data = await db.longmsg.find_one({"chat_id": chat_id})
    return data.get("limit", 800) if data else 800

# ==========================================================
# phone 📱 
# ==========================================================

async def set_nophone_status(chat_id, status):
    await db.nophone.update_one({"chat_id": chat_id}, {"$set": {"enabled": status}}, upsert=True)
async def get_nophone_status(chat_id):
    data = await db.nophone.find_one({"chat_id": chat_id})
    return bool(data.get("enabled", False)) if data else False

# ==========================================================
# Hashtag 🔤 
# ==========================================================

async def set_nohashtag_status(chat_id, status):
    await db.nohashtag.update_one({"chat_id": chat_id}, {"$set": {"enabled": status}}, upsert=True)
async def get_nohashtag_status(chat_id):
    data = await db.nohashtag.find_one({"chat_id": chat_id})
    return bool(data.get("enabled", False)) if data else False

# ==========================================================
# 🛂 command 
# ==========================================================

async def set_cmddeleter_status(chat_id: int, status: bool):
    await db.cmddeleter.update_one({"chat_id": chat_id}, {"$set": {"enabled": status}}, upsert=True)

async def get_cmddeleter_status(chat_id: int) -> bool:
    data = await db.cmddeleter.find_one({"chat_id": chat_id})
    return bool(data.get("enabled", False)) if data else False

# ==========================================================
# 🖼️ media deleter 
# ==========================================================
async def set_mediadelete_status(chat_id: int, status: bool):
    await db.mediadelete.update_one({"chat_id": chat_id}, {"$set": {"enabled": status}}, upsert=True)

async def get_mediadelete_status(chat_id: int) -> bool:
    data = await db.mediadelete.find_one({"chat_id": chat_id})
    return bool(data.get("enabled", False)) if data else False

async def set_mediadelay(chat_id: int, seconds: int):
    await db.mediadelete.update_one({"chat_id": chat_id}, {"$set": {"delay": seconds}}, upsert=True)

async def get_mediadelay(chat_id: int) -> int:
    data = await db.mediadelete.find_one({"chat_id": chat_id})
    return data.get("delay", 300) if data else 300


# ==========================================================
# 💬 Messege deleter 
# ==========================================================
async def set_cleaner_status(chat_id: int, status: bool):
    await db.cleaner.update_one({"chat_id": chat_id}, {"$set": {"enabled": status}}, upsert=True)

async def get_cleaner_status(chat_id: int) -> bool:
    data = await db.cleaner.find_one({"chat_id": chat_id})
    return bool(data.get("enabled", False)) if data else False

async def set_cleandelay(chat_id: int, seconds: int):
    await db.cleaner.update_one({"chat_id": chat_id}, {"$set": {"delay": seconds}}, upsert=True)

async def get_cleandelay(chat_id: int) -> int:
    data = await db.cleaner.find_one({"chat_id": chat_id})
    return data.get("delay", 300) if data else 300


# ==========================================================
# 🚫 BLACKLIST 
# ==========================================================

async def add_blacklist_word(chat_id: int, word: str):
    await db.blacklist.update_one({"chat_id": chat_id}, {"$addToSet": {"words": word}}, upsert=True)

async def remove_blacklist_word(chat_id: int, word: str) -> bool:
    result = await db.blacklist.update_one({"chat_id": chat_id}, {"$pull": {"words": word}})
    return result.modified_count > 0

async def get_blacklist(chat_id: int) -> list:
    data = await db.blacklist.find_one({"chat_id": chat_id})
    return data.get("words", []) if data else []

# ==========================================================
# 🔮 Filters
# ==========================================================

async def set_filter(chat_id: int, keyword: str, content_type: str, content: str, file_id: str):
    await db.filters.update_one(
        {"chat_id": chat_id},
        {"$set": {f"filters.{keyword}": {"type": content_type, "content": content, "file_id": file_id}}},
        upsert=True
    )

async def delete_filter(chat_id: int, keyword: str) -> bool:
    result = await db.filters.update_one({"chat_id": chat_id}, {"$unset": {f"filters.{keyword}": ""}})
    return result.modified_count > 0

async def get_all_filters(chat_id: int) -> dict:
    data = await db.filters.find_one({"chat_id": chat_id})
    return data.get("filters", {}) if data else {}

# ==========================================================
# 👭 Join Request 
# ==========================================================

async def set_acceptall_status(chat_id: int, status: bool):
    await db.joinrequest.update_one({"chat_id": chat_id}, {"$set": {"enabled": status}}, upsert=True)

async def get_acceptall_status(chat_id: int) -> bool:
    data = await db.joinrequest.find_one({"chat_id": chat_id})
    return bool(data.get("enabled", False)) if data else False

# ==========================================================
# 👻 Ghost Mode
# ==========================================================

async def set_ghost_status(chat_id: int, status: bool):
    await db.ghost.update_one({"chat_id": chat_id}, {"$set": {"enabled": status}}, upsert=True)

async def get_ghost_status(chat_id: int) -> bool:
    data = await db.ghost.find_one({"chat_id": chat_id})
    return bool(data.get("enabled", False)) if data else False
