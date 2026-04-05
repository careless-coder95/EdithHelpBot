<div align="center">

<img src="https://files.catbox.moe/j2yhce.jpg" width="200" style="border-radius: 50%"/>

# 🤖 EdithHelpBot

**A Powerful Telegram Group Manager Bot**

[![Author](https://img.shields.io/badge/Author-Mr.%20Stark-blue?style=for-the-badge&logo=telegram)](https://t.me/CarelessxOwner)
[![Support](https://img.shields.io/badge/Support-Group-green?style=for-the-badge&logo=telegram)](https://t.me/ll_CarelessxCoder_ll)
[![Updates](https://img.shields.io/badge/Updates-Channel-red?style=for-the-badge&logo=telegram)](https://t.me/ll_CarelessxCoder_ll)
[![Demo Bot](https://img.shields.io/badge/Demo-Bot-purple?style=for-the-badge&logo=telegram)](https://t.me/EdithHelpsBot)
[![Python](https://img.shields.io/badge/Python-3.10+-yellow?style=for-the-badge&logo=python)](https://python.org)
[![Pyrogram](https://img.shields.io/badge/Pyrogram-2.0.106-blue?style=for-the-badge)](https://pyrogram.org)

</div>

---

## ✨ Features

<details>
<summary><b>🔒 Lock System</b></summary>

| Command | Description |
|---|---|
| `/lock url` | Block links/URLs |
| `/lock text` | Block ALL text messages |
| `/lock sticker` | Block stickers |
| `/lock media` | Block photos/videos/docs |
| `/lock username` | Block @mentions |
| `/lock forward` | Block forwarded messages |
| `/lock edit` | Delete edited messages |
| `/unlock <type>` | Remove a lock |
| `/locks` | Show active locks |
| `/lockall` | Lock everything at once 🔐 |
| `/unlockall` | Unlock everything at once 🔓 |

</details>

<details>
<summary><b>👮 Moderation</b></summary>

| Command | Description |
|---|---|
| `/ban` / `/unban` | Ban or unban a user |
| `/kick` | Remove user from group |
| `/mute` / `/unmute` | Mute or unmute a user |
| `/warn` | Give warning (3 = auto mute) |
| `/warns` | Check warnings |
| `/resetwarns` | Reset warnings |
| `/promote` / `/demote` | Make or remove admin |

</details>

<details>
<summary><b>👋 Greetings</b></summary>

| Command | Description |
|---|---|
| `/welcome on/off` | Enable/disable welcome |
| `/setwelcome <text>` | Set custom welcome message |

**Placeholders:** `{first_name}` `{username}` `{mention}` `{title}`

</details>

<details>
<summary><b>📝 Notes</b></summary>

| Command | Description |
|---|---|
| `/setnote <name> <text>` | Save a note |
| `/delnote <name>` | Delete a note |
| `/notes` | List all notes with private links |
| `#note_name` | Get note link in group |

</details>

<details>
<summary><b>📜 Rules</b></summary>

| Command | Description |
|---|---|
| `/setrules <text>` | Set group rules (formatting preserved) |
| `/rules` | Show rules |
| `/clearrules` | Remove all rules |

</details>

<details>
<summary><b>🔗 BioLink Protection</b></summary>

| Command | Description |
|---|---|
| `/biolink on` | Block users with links in bio |
| `/biolink off` | Disable protection |

</details>

<details>
<summary><b>🤬 Abuse Detection</b></summary>

| Command | Description |
|---|---|
| `/noabuse on` | Enable abuse filter |
| `/noabuse off` | Disable abuse filter |

</details>

<details>
<summary><b>📢 Force Subscribe</b></summary>

| Command | Description |
|---|---|
| `/addfsub @channel` | Add a required channel |
| `/removefsub @channel` | Remove a channel |
| `/fsublist` | List all required channels |

</details>

<details>
<summary><b>🛠️ Tools</b></summary>

| Command | Description |
|---|---|
| `/echo <text>` | Echo text, auto Telegraph if too long |
| `/setlongmode off/manual/automatic` | Set long message mode |
| `/setlonglimit <200-4000>` | Set character limit (default 800) |
| `/nophone on/off` | Block phone numbers |
| `/nohashtags on/off` | Block hashtags |

</details>

<details>
<summary><b>⚙️ Utility</b></summary>

| Command | Description |
|---|---|
| `/chatinfo` | Group details & member count |
| `/id` | Your ID or replied user's ID |
| `/pin` | Pin a replied message |
| `/unpin` | Unpin a message or all pins |
| `/purge` | Bulk delete messages |
| `/del` | Delete a specific replied message |
| `/report` | Report a user to admins |

</details>

<details>
<summary><b>🗑️ Command Deleter</b></summary>

| Command | Description |
|---|---|
| `/cmd on` | Auto delete all commands |
| `/cmd off` | Disable command deleter |

Deletes any message starting with `/` `!` `.`

</details>

<details>
<summary><b>🗑️ Media Cleaner</b></summary>

| Command | Description |
|---|---|
| `/mediadelete on` | Auto delete Media at default (5m) time. |
| `/mediadelete off` | Disable Auto Media delete  |
| `/setmediadelay <time>` | Set You Custom Time To Delete Media |

</details>

---

## 📁 File Structure

```
NomadeHelpBot/
│
├── main.py
├── config.py
├── db.py
├── security.py
├── requirements.txt
├── .env                  ← API keys yahan
│
└── handlers/
    ├── __init__.py
    ├── start.py          ← Start, Help menu, Callbacks
    ├── group_commands.py ← Locks, BioLink, Moderation, Welcome
    ├── notes.py          ← Notes system
    ├── rules.py          ← Rules system
    ├── abuse.py          ← Abuse detection
    ├── fsub.py           ← Force subscribe
    ├── tools.py          ← Echo, LongMsg, Phone, Hashtag
    ├── utility.py        ← ChatInfo, Pin, Purge, Report
    ├── cmddeleter.py     ← Command auto-delete
    └── mediadelete.py    ← Auto media Cleaner 
```
---

## ⚙️ Setup

### Prerequisites

- Python 3.10+
- MongoDB Atlas account (free)
- Telegram API credentials

### Step 1 — Get Credentials

| Field | Source |
|---|---|
| `API_ID` & `API_HASH` | [my.telegram.org](https://my.telegram.org) |
| `BOT_TOKEN` | [@BotFather](https://t.me/BotFather) |
| `MONGO_URI` | [MongoDB Atlas](https://cloud.mongodb.com) |
| `OWNER_ID` | [@userinfobot](https://t.me/userinfobot) |

### Step 2 — Fill `.env`

```env
API_ID=12345678
API_HASH=abcdef1234567890abcdef1234567890
BOT_TOKEN=123456789:AABBccDDeeFFggHH
MONGO_URI=mongodb+srv://user:pass@cluster0.mongodb.net/
DB_NAME=Cluster0
OWNER_ID=123456789
BOT_USERNAME=YourBotUsername
SUPPORT_GROUP=https://t.me/ll_CarelessxCoder_ll
UPDATE_CHANNEL=https://t.me/ll_CarelessxCoder_ll
START_IMAGE=https://files.catbox.moe/j2yhce.jpg
```

---

## 🚀 Deployment

<details>
<summary><b>🖥️ VPS Deployment</b></summary>

### Step 1 — Server Setup
```bash
# System update karo
sudo apt update && sudo apt upgrade -y

# Python install karo
sudo apt install python3 python3-pip git -y
```

### Step 2 — Bot Clone karo
```bash
git clone https://github.com/YourRepo/NomadeHelpBot.git
cd NomadeHelpBot
```

### Step 3 — Dependencies install karo
```bash
pip3 install -r requirements.txt
```

### Step 4 — `.env` fill karo
```bash
nano .env
# Apni values paste karo, Ctrl+X → Y → Enter
```

### Step 5 — Bot run karo (background mein)
```bash
# screen se run karo taaki close karne par band na ho
sudo apt install screen -y
screen -S nomade
python3 main.py

# Screen se bahar aane ke liye: Ctrl+A → D
# Wapas aane ke liye: screen -r nomade
```

### Auto-restart setup (systemd)
```bash
sudo nano /etc/systemd/system/nomade.service
```
```ini
[Unit]
Description=NomadeHelpBot
After=network.target

[Service]
User=root
WorkingDirectory=/root/NomadeHelpBot
ExecStart=/usr/bin/python3 main.py
Restart=always

[Install]
WantedBy=multi-user.target
```
```bash
sudo systemctl enable nomade
sudo systemctl start nomade
sudo systemctl status nomade
```

</details>

<details>
<summary><b>🟣 Heroku Deployment</b></summary>

### Step 1 — Heroku Account
- [heroku.com](https://heroku.com) par account banao
- Heroku CLI install karo

### Step 2 — Login & App Create
```bash
heroku login
heroku create your-nomade-bot
```

### Step 3 — Config Variables Set karo
```bash
heroku config:set API_ID=12345678
heroku config:set API_HASH=abcdef...
heroku config:set BOT_TOKEN=123456...
heroku config:set MONGO_URI=mongodb+srv://...
heroku config:set DB_NAME=Cluster0
heroku config:set OWNER_ID=123456789
heroku config:set BOT_USERNAME=YourBotUsername
heroku config:set SUPPORT_GROUP=https://t.me/ll_CarelessxCoder_ll
heroku config:set UPDATE_CHANNEL=https://t.me/ll_CarelessxCoder_ll
heroku config:set START_IMAGE=https://files.catbox.moe/j2yhce.jpg
```

### Step 4 — Deploy karo
```bash
git init
git add .
git commit -m "Deploy NomadeHelpBot"
heroku git:remote -a your-nomade-bot
git push heroku main
```

### Step 5 — Worker on karo
```bash
heroku ps:scale worker=1
```

> ⚠️ **Note:** `Procfile` already included hai — `worker: python3 main.py`

</details>

<details>
<summary><b>🟦 Render Deployment</b></summary>

### Step 1 — Render Account
- [render.com](https://render.com) par account banao
- GitHub par apna bot push karo

### Step 2 — New Service
1. Dashboard mein **"New +"** click karo
2. **"Background Worker"** select karo
3. Apna GitHub repo connect karo

### Step 3 — Settings
| Field | Value |
|---|---|
| **Name** | nomade-help-bot |
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python3 main.py` |

### Step 4 — Environment Variables
Render dashboard mein **"Environment"** tab mein yeh sab add karo:

```
API_ID          = 12345678
API_HASH        = abcdef...
BOT_TOKEN       = 123456...
MONGO_URI       = mongodb+srv://...
DB_NAME         = Cluster0
OWNER_ID        = 123456789
BOT_USERNAME    = YourBotUsername
SUPPORT_GROUP   = https://t.me/ll_CarelessxCoder_ll
UPDATE_CHANNEL  = https://t.me/ll_CarelessxCoder_ll
START_IMAGE     = https://files.catbox.moe/j2yhce.jpg
```

### Step 5 — Deploy
**"Create Background Worker"** click karo — Render automatically deploy karega!

> ✅ Render free tier mein bhi kaam karta hai. Auto-deploy on push bhi enable kar sakte ho.

</details>

---

## 📞 Contact

<div align="center">

| | |
|---|---|
| 👤 **Author** | [Mr. Stark](https://t.me/CarelessxOwner) |
| 💬 **Support** | [CarelessxCoder](https://t.me/ll_CarelessxCoder_ll) |
| 📢 **Updates** | [CarelessxCoder Channel](https://t.me/ll_CarelessxCoder_ll) |

</div>

---

<div align="center">

Made with ❤️ by **Mr. Stark**

</div>
