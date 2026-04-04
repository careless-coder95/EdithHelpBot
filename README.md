# 🤖 NomadeHelpBot

**A powerful Telegram Group Manager Bot**
Built with ❤️ by **Mr. Stark**

---

## ✨ Features

- 🔒 Advanced Lock System (text, url, media, sticker, forward, edit)
- 🔗 BioLink Protection
- 📝 Notes System with private deep links
- 📜 Rules Management (exact formatting preserved)
- 👮 Full Moderation (ban, kick, mute, warn, promote, demote)
- 👋 Custom Welcome Messages
- 📢 Broadcast to all users
- 💾 MongoDB powered — persistent data

---

## 📁 File Structure

```
NomadeHelpBot/
│
├── main.py              # Bot ka entry point
├── config.py            # Environment variables loader
├── db.py                # MongoDB database functions
├── security.py          # (Placeholder — no restrictions)
├── requirements.txt     # Python dependencies
├── Procfile             # Heroku deployment
├── Dockerfile           # Docker deployment
├── .env                 # ← Aapki API keys yahan daalni hain
│
└── handlers/
    ├── __init__.py      # Sabke handlers register karta hai
    ├── start.py         # /start, help menu, callbacks
    ├── group_commands.py# Locks, BioLink, Moderation, Welcome
    ├── notes.py         # Notes system
    ├── rules.py         # Rules system
    └── repo.py          # Repo handler
```

---

## ⚙️ Setup — Step by Step

### Step 1 — Credentials Hasil Karo

| Cheez | Kahan Se |
|---|---|
| `API_ID` & `API_HASH` | [my.telegram.org](https://my.telegram.org) → API Development |
| `BOT_TOKEN` | Telegram par [@BotFather](https://t.me/BotFather) se |
| `MONGO_URI` | [MongoDB Atlas](https://cloud.mongodb.com) — free cluster |
| `OWNER_ID` | [@userinfobot](https://t.me/userinfobot) se apna ID lao |

### Step 2 — `.env` File Fill Karo

```env
API_ID=12345678
API_HASH=abcdef1234567890abcdef1234567890
BOT_TOKEN=123456789:AABBccDDeeFFggHHiiJJkkLLmmNNoo
MONGO_URI=mongodb+srv://user:pass@cluster0.mongodb.net/
DB_NAME=Cluster0
OWNER_ID=123456789
BOT_USERNAME=YourBotUsername
SUPPORT_GROUP=https://t.me/YourGroup
UPDATE_CHANNEL=https://t.me/YourChannel
START_IMAGE=https://files.catbox.moe/j2yhce.jpg
```

### Step 3 — Dependencies Install Karo

```bash
pip install -r requirements.txt
```

### Step 4 — Bot Run Karo

```bash
python main.py
```

---

## 🚀 Deploy on Railway / Render / VPS

1. Saari files upload karo
2. `.env` variables set karo platform ke settings mein
3. Start command: `python main.py`

---

## 🤖 Bot Commands

### 🔒 Locks
| Command | Kaam |
|---|---|
| `/lock text` | Koi bhi text message nahi kar payega |
| `/lock edit` | Edited messages turant delete honge |
| `/lock url` | Links block |
| `/lock sticker` | Stickers block |
| `/lock media` | Photos/Videos block |
| `/lock forward` | Forwarded messages block |
| `/unlock <type>` | Lock hatao |
| `/locks` | Active locks dekho |

### 📝 Notes
| Command | Kaam |
|---|---|
| `/setnote <n> <text>` | Note save karo |
| `/delnote <n>` | Note delete karo |
| `/notes` | Sabke notes ki list (private links ke saath) |
| `#note_name` | Group mein hashtag type karo — link milega |

### 📜 Rules
| Command | Kaam |
|---|---|
| `/setrules <text>` | Rules set karo (formatting preserve hoti hai) |
| `/rules` | Rules dikhao |
| `/clearrules` | Rules clear karo |

### 🔗 BioLink
| Command | Kaam |
|---|---|
| `/biolink on` | Bio me link wale ka message delete hoga |
| `/biolink off` | Protection off karo |

### 👮 Moderation
| Command | Kaam |
|---|---|
| `/ban` / `/unban` | Ban/Unban user |
| `/kick` | User ko group se hatao |
| `/mute` / `/unmute` | Chup karao / Bolne do |
| `/warn` | Warning do (3 = auto mute) |
| `/warns` | Warnings check karo |
| `/resetwarns` | Warns reset karo |
| `/promote` / `/demote` | Admin banao / hatao |

### 👋 Greetings
| Command | Kaam |
|---|---|
| `/welcome on/off` | Welcome on/off karo |
| `/setwelcome <text>` | Custom welcome set karo |

---

## 📞 Support

Koi bhi problem ho toh feel free to reach out to **Mr. Stark**

