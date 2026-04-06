<div align="center">

<img src="https://files.catbox.moe/j2yhce.jpg" width="180" style="border-radius: 50%; border: 3px solid #7289da"/>

<br>

# ✦ EDITH HELP BOT ✦

> *Powerful • Fast • Reliable*

<br>

[![Demo Bot](https://img.shields.io/badge/🤖_Demo-Bot-7289da?style=for-the-badge)](https://t.me/EdithHelpsBot)
[![Author](https://img.shields.io/badge/👤_Author-Mr.%20Stark-ff6b6b?style=for-the-badge)](https://t.me/CarelessxOwner)
[![Support](https://img.shields.io/badge/💬_Support-Group-43b581?style=for-the-badge)](https://t.me/ll_CarelessxCoder_ll)
[![Updates](https://img.shields.io/badge/📢_Updates-Channel-faa61a?style=for-the-badge)](https://t.me/ll_CarelessxCoder_ll)

<br>

[![Python](https://img.shields.io/badge/Python-3.10+-3776ab?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Pyrogram](https://img.shields.io/badge/Pyrogram-2.0.106-2b7bb9?style=flat-square)](https://pyrogram.org)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47a248?style=flat-square&logo=mongodb&logoColor=white)](https://cloud.mongodb.com)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE.md)

</div>

---

<div align="center">

```
╔══════════════════════════════════════════════════════╗
║                                                      ║
║   A next-gen Telegram Group Manager Bot              ║
║   built with Pyrogram & MongoDB                      ║
║   Packed with powerful moderation tools              ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
```

</div>

---

## ⚡ Features

<details>
<summary><b>🔒 Lock System</b></summary>
<br>

| Command | Description |
|:---|:---|
| `/lock <type>` | Lock a specific type |
| `/unlock <type>` | Unlock a specific type |
| `/locks` | Show all active locks |
| `/lockall` | Lock everything at once 🔐 |
| `/unlockall` | Unlock everything at once 🔓 |

**Available lock types:**
`url` • `text` • `sticker` • `media` • `username` • `forward` • `edit`

</details>

<details>
<summary><b>👮 Moderation</b></summary>
<br>

| Command | Description |
|:---|:---|
| `/ban` / `/unban` | Ban or unban a user |
| `/kick` | Remove user from group |
| `/mute` / `/unmute` | Mute or unmute a user |
| `/tmute <time>` | Temporarily mute (1m–24h) |
| `/tban <time>` | Temporarily ban (1m–24h) |
| `/warn` | Give a warning (3 = auto mute) |
| `/warns` | Check warnings |
| `/resetwarns` | Reset all warnings |

</details>

<details>
<summary><b>👑 Promote System</b></summary>
<br>

| Command | Description |
|:---|:---|
| `/promote <user>` | Standard admin |
| `/mod <user>` | Moderator role |
| `/fullpromote <user>` | Full admin (all powers) |
| `/demote <user>` | Remove admin rights |

> 💡 Custom title support: `/promote @user Manager`

</details>

<details>
<summary><b>👋 Greetings</b></summary>
<br>

| Command | Description |
|:---|:---|
| `/welcome on/off` | Toggle welcome messages |
| `/setwelcome <text>` | Set custom welcome message |

**Placeholders:** `{first_name}` `{username}` `{mention}` `{title}`

</details>

<details>
<summary><b>📝 Notes</b></summary>
<br>

| Command | Description |
|:---|:---|
| `/setnote <name> <text>` | Save a note |
| `/delnote <name>` | Delete a note |
| `/notes` | List all notes with private links |
| `#note_name` | Get note link in group |

</details>

<details>
<summary><b>📜 Rules</b></summary>
<br>

| Command | Description |
|:---|:---|
| `/setrules <text>` | Set group rules |
| `/rules` | Show current rules |
| `/clearrules` | Remove all rules |

> ✅ Exact formatting preserved — spaces, newlines, everything.

</details>

<details>
<summary><b>🔗 BioLink Protection</b></summary>
<br>

| Command | Description |
|:---|:---|
| `/biolink on` | Block users with links in bio |
| `/biolink off` | Disable protection |

</details>

<details>
<summary><b>🤬 Abuse Detection</b></summary>
<br>

| Command | Description |
|:---|:---|
| `/noabuse on` | Enable abuse word filter |
| `/noabuse off` | Disable abuse filter |

</details>

<details>
<summary><b>📢 Force Subscribe</b></summary>
<br>

| Command | Description |
|:---|:---|
| `/addfsub @channel` | Add a required channel |
| `/removefsub @channel` | Remove a channel |
| `/fsublist` | List all required channels |

</details>

<details>
<summary><b>🛠️ Tools</b></summary>
<br>

| Command | Description |
|:---|:---|
| `/echo <text>` | Echo text — auto Telegraph if too long |
| `/setlongmode off/manual/automatic` | Handle long messages |
| `/setlonglimit <200–4000>` | Set character limit (default 800) |
| `/nophone on/off` | Block phone numbers |
| `/nohashtags on/off` | Block hashtags |

</details>

<details>
<summary><b>⚙️ Utility</b></summary>
<br>

| Command | Description |
|:---|:---|
| `/chatinfo` | Group details & member count |
| `/id` | Your ID or replied user's ID |
| `/pin` / `/unpin` | Pin or unpin messages |
| `/purge` | Bulk delete messages |
| `/del` | Delete a specific replied message |
| `/report` | Report a user to admins |

</details>

<details>
<summary><b>🗑️ Command Deleter</b></summary>
<br>

| Command | Description |
|:---|:---|
| `/cmd on` | Auto delete all commands |
| `/cmd off` | Disable command deleter |

> Deletes any message starting with `/` `!` `.`

</details>

<details>
<summary><b>🎬 Media Auto-Delete</b></summary>
<br>

| Command | Description |
|:---|:---|
| `/mediadelete on/off` | Toggle media auto-delete |
| `/setmediadelay <time>` | Set delay (1m–24h) |

> Applies to photos, videos, stickers, GIFs, animations, polls and locations.

</details>

<details>
<summary><b>🧹 Message Cleaner</b></summary>
<br>

| Command | Description |
|:---|:---|
| `/cleaner on/off` | Toggle message cleaner |
| `/setcleandelay <time>` | Set delay (1m–24h) |
| `/cleanstatus` | Show current settings |

> Auto-deletes all regular user messages after set delay. Admin messages are never deleted.

</details>

<details>
<summary><b>🧟 Zombie Remover</b></summary>
<br>

| Command | Description |
|:---|:---|
| `/zombie` | Scan and remove all deleted accounts |

</details>

<details>
<summary><b>📢 Tag All</b></summary>
<br>

| Command | Description |
|:---|:---|
| `/tagall` | Mention all group members |
| `/tagall <message>` | Mention all with a custom message |
| `/stop` | Stop tagging immediately |

</details>

---

## 📁 File Structure

```
EdithHelpBot/
│
├── main.py                   ← Entry point
├── config.py                 ← Load environment variables
├── db.py                     ← MongoDB database functions
├── security.py               ← Security placeholder
├── requirements.txt          ← Python dependencies
├── Procfile                  ← Heroku deployment
├── Dockerfile                ← Docker deployment
├── .env                      ← ⚠️ Your API keys go here
│
└── handlers/
    ├── __init__.py           ← Register all handlers
    ├── start.py              ← Start, Help menu, Callbacks
    ├── group_commands.py     ← Locks, BioLink, Moderation, Welcome
    ├── promote.py            ← Promote, Mod, FullPromote, Demote
    ├── notes.py              ← Notes system
    ├── rules.py              ← Rules system
    ├── abuse.py              ← Abuse word detection
    ├── fsub.py               ← Force subscribe
    ├── tools.py              ← Echo, LongMsg, Phone, Hashtag
    ├── utility.py            ← ChatInfo, Pin, Purge, Report
    ├── cmddeleter.py         ← Command auto-delete
    ├── mediadelete.py        ← Media auto-delete
    ├── cleaner.py            ← Message cleaner
    ├── zombie.py             ← Zombie account remover
    └── tagall.py             ← Tag all members
```

---

## ⚙️ Setup

### Step 1 — Get Credentials

| Field | Where to get |
|:---|:---|
| `API_ID` & `API_HASH` | [my.telegram.org](https://my.telegram.org) → API Development |
| `BOT_TOKEN` | [@BotFather](https://t.me/BotFather) on Telegram |
| `MONGO_URI` | [MongoDB Atlas](https://cloud.mongodb.com) — Free cluster |
| `OWNER_ID` | [@userinfobot](https://t.me/userinfobot) |

### Step 2 — Fill `.env` File

```env
API_ID=12345678
API_HASH=abcdef1234567890abcdef1234567890
BOT_TOKEN=123456789:AABBccDDeeFFggHH
MONGO_URI=mongodb+srv://user:pass@cluster0.mongodb.net/
DB_NAME=Cluster0
OWNER_ID=123456789
BOT_USERNAME=EdithHelpsBot
SUPPORT_GROUP=https://t.me/ll_CarelessxCoder_ll
UPDATE_CHANNEL=https://t.me/ll_CarelessxCoder_ll
START_IMAGE=https://files.catbox.moe/j2yhce.jpg
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Run

```bash
python main.py
```

---

## 🚀 Deployment

<details>
<summary><b>🖥️ VPS Deployment</b></summary>
<br>

### 1 — Server Setup
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip git screen -y
```

### 2 — Clone & Setup
```bash
git clone https://github.com/careless-coder95/EdithHelpBot.git
cd EdithHelpBot
pip3 install -r requirements.txt
```

### 3 — Configure
```bash
nano .env
# Fill in your values → Ctrl+X → Y → Enter
```

### 4 — Run in Background
```bash
screen -S edith
python3 main.py
# Detach: Ctrl+A → D
# Reattach: screen -r edith
```

### 5 — Auto Restart (systemd)
```bash
sudo nano /etc/systemd/system/edith.service
```
```ini
[Unit]
Description=EdithHelpBot
After=network.target

[Service]
User=root
WorkingDirectory=/root/EdithHelpBot
ExecStart=/usr/bin/python3 main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```
```bash
sudo systemctl daemon-reload
sudo systemctl enable edith
sudo systemctl start edith
sudo systemctl status edith
```

</details>

<details>
<summary><b>🟣 Heroku Deployment</b></summary>
<br>

### 1 — Install Heroku CLI & Login
```bash
# Install: https://devcenter.heroku.com/articles/heroku-cli
heroku login
```

### 2 — Create App
```bash
heroku create edith-help-bot
```

### 3 — Set Config Vars
```bash
heroku config:set API_ID=12345678
heroku config:set API_HASH=abcdef...
heroku config:set BOT_TOKEN=123456...
heroku config:set MONGO_URI=mongodb+srv://...
heroku config:set DB_NAME=Cluster0
heroku config:set OWNER_ID=123456789
heroku config:set BOT_USERNAME=EdithHelpsBot
heroku config:set SUPPORT_GROUP=https://t.me/ll_CarelessxCoder_ll
heroku config:set UPDATE_CHANNEL=https://t.me/ll_CarelessxCoder_ll
heroku config:set START_IMAGE=https://files.catbox.moe/j2yhce.jpg
```

### 4 — Deploy
```bash
git init
git add .
git commit -m "Deploy EdithHelpBot"
heroku git:remote -a edith-help-bot
git push heroku main
```

### 5 — Start Worker
```bash
heroku ps:scale worker=1
```

> ✅ `Procfile` is already included — `worker: python3 main.py`

</details>

<details>
<summary><b>🟦 Render Deployment</b></summary>
<br>

### 1 — Prepare
- Create account at [render.com](https://render.com)
- Push your bot to GitHub

### 2 — Create New Service
1. Dashboard → **New +**
2. Select **Background Worker**
3. Connect your GitHub repo

### 3 — Configure Service

| Field | Value |
|:---|:---|
| **Name** | edith-help-bot |
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python3 main.py` |

### 4 — Set Environment Variables

Go to **Environment** tab and add:

```
API_ID              = 12345678
API_HASH            = abcdef...
BOT_TOKEN           = 123456...
MONGO_URI           = mongodb+srv://...
DB_NAME             = Cluster0
OWNER_ID            = 123456789
BOT_USERNAME        = EdithHelpsBot
SUPPORT_GROUP       = https://t.me/ll_CarelessxCoder_ll
UPDATE_CHANNEL      = https://t.me/ll_CarelessxCoder_ll
START_IMAGE         = https://files.catbox.moe/j2yhce.jpg
```

### 5 — Deploy
Click **Create Background Worker** — Render will auto-deploy!

> ✅ Free tier works. Auto-deploy on every git push can be enabled.

</details>

---

## 📞 Contact

<div align="center">

| | |
|:---:|:---:|
| 👤 **Author** | [Mr. Stark](https://t.me/CarelessxOwner) |
| 💬 **Support** | [CarelessxCoder](https://t.me/ll_CarelessxCoder_ll) |
| 📢 **Updates** | [CarelessxCoder Channel](https://t.me/ll_CarelessxCoder_ll) |
| 🤖 **Demo Bot** | [EdithHelpsBot](https://t.me/EdithHelpsBot) |
| 💻 **Repository** | [GitHub](https://github.com/careless-coder95/EdithHelpBot) |

</div>

---

<div align="center">

```
╔══════════════════════════════╗
║   Made with ❤️ by Mr. Stark  ║
╚══════════════════════════════╝
```

⭐ **Star this repo if you found it useful!** ⭐

</div>
