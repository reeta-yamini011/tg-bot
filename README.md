# Telegram Bot (PostgreSQL + Real Broadcast)

A **production-ready Telegram bot template** built with **python-telegram-bot (async)** and **PostgreSQL**, featuring real user tracking, admin tools, and safe broadcasting to all users.

---

## ✨ Features

- Async Telegram bot (`python-telegram-bot v21`)
- PostgreSQL with **SQLAlchemy 2.0 (async)**
- Real broadcast to all users (stores `chat_id`)
- Admin-only commands
- Handles blocked users gracefully
- User tracking middleware
- Clean, scalable folder structure
- Docker & Docker Compose support

---

## 📁 Project Structure

```
tg-bot/
├── bot/
│   ├── __main__.py
│   ├── core/
│   │   ├── app.py
│   │   ├── config.py
│   │   └── logging.py
│   ├── db/
│   │   ├── engine.py
│   │   ├── models.py
│   │   └── repo.py
│   ├── handlers/
│   │   ├── admin.py
│   │   ├── common.py
│   │   ├── errors.py
│   │   └── messages.py
│   ├── middlewares/
│   │   └── user_tracker.py
│   └── services/
│       └── broadcaster.py
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 🚀 Getting Started

### 1. Create a Telegram Bot

- Open **@BotFather**
- Create a new bot
- Copy the **BOT_TOKEN**

---

### 2. Environment Variables

Create a `.env` file in the project root:

```
BOT_TOKEN=123456789:YOUR_BOT_TOKEN
ADMIN_IDS=123456789,987654321
LOG_LEVEL=INFO
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/tgbot
```

---

## 🐳 Run with Docker (Recommended)

```
docker compose up --build
```

---

## 💻 Run Locally

```
pip install -r requirements.txt
cp .env.example .env
python -m bot
```

---

## 🤖 Bot Commands

### Public
- /start
- /help
- /ping
- /about

### Admin
- /stats
- /broadcast <message>
- /broadcast_copy
