import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import sqlite3
from datetime import datetime, timedelta
import threading
import time

import os
TOKEN = os.getenv("TOKEN")
ADMIN_ID = 123456789

bot = telebot.TeleBot(TOKEN)

conn = sqlite3.connect("data.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER,
    username TEXT,
    date TEXT,
    completed TEXT,
    streak INTEGER
)
""")
conn.commit()

challenges = [
    "Gazsiz ichimliklar",
    "Tongda detox",
    "Sugar detox",
    "5000 sarmoya",
    "Kitob 20 min",
    "Badantarbiya",
    "1 daqiqa tinchlik"
]

def keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for c in challenges:
        kb.add(KeyboardButton(c))
    kb.add(KeyboardButton("Finish"))
    return kb

def today():
    return datetime.now().strftime("%Y-%m-%d")

def get_user(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id=? AND date=?", (user_id, today()))
    return cursor.fetchone()

def save(user_id, username, data, streak):
    cursor.execute("DELETE FROM users WHERE user_id=? AND date=?", (user_id, today()))
    cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)",
                   (user_id, username, today(), "|".join(data), streak))
    conn.commit()

def get_all_today():
    cursor.execute("SELECT user_id, username, completed FROM users WHERE date=?", (today(),))
    return cursor.fetchall()

@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id, "Challenge boshlandi 🔥", reply_markup=keyboard())

@bot.message_handler(func=lambda m: True)
def handle(msg):
    user = msg.chat.id
    username = msg.from_user.username or msg.from_user.first_name

    row = get_user(user)

    if row:
        data = row[3].split("|") if row[3] else []
        streak = row[4]
    else:
        data = []
        streak = 0

    if msg.text == "Finish":
        percent = int(len(data)/len(challenges)*100)

        # streak logika
        if percent == 100:
            streak += 1
        else:
            streak = 0

        save(user, username, data, streak)

        bot.send_message(user, f"📊 {percent}% bajarildi\n🔥 Streak: {streak} kun")
        return

    if msg.text in challenges:
        if msg.text not in data:
            data.append(msg.text)
            save(user, username, data, streak)
            bot.send_message(user, f"✅ {msg.text}")
        else:
            bot.send_message(user, "Oldin belgilangan")

# ADMIN PANEL
@bot.message_handler(commands=['admin'])
def admin(msg):
    if msg.chat.id != ADMIN_ID:
        return

    users = get_all_today()

    leaderboard = []
    text = "🏆 Leaderboard:\n"

    for u in users:
        comp = u[2].split("|") if u[2] else []
        percent = int(len(comp)/len(challenges)*100)
        leaderboard.append((u[1], percent))

    leaderboard.sort(key=lambda x: x[1], reverse=True)

    for i, (name, p) in enumerate(leaderboard[:10], 1):
        text += f"{i}. @{name} — {p}%\n"

    bot.send_message(msg.chat.id, text)

# ⏰ ESLATMA (HAR KUNI)
def reminder():
    while True:
        now = datetime.now().strftime("%H:%M")

        if now == "20:00":
            users = get_all_today()
            for u in users:
                try:
                    bot.send_message(u[0], "⏰ Challenge eslatma! Bugungi vazifalarni bajardingmi?")
                except:
                    pass

            time.sleep(60)

        time.sleep(10)

# 📊 HAFTALIK REPORT
def weekly_report():
    while True:
        now = datetime.now()
        # Yakshanba 21:00
        if now.weekday() == 6 and now.strftime("%H:%M") == "21:00":
            cursor.execute("SELECT username, COUNT(*) FROM users GROUP BY username")
            data = cursor.fetchall()
            
            text = "📊 Haftalik report:\n"
            for d in data:
                text += f"@{d[0]} — {d[1]} kun faol\n"
            
            bot.send_message(ADMIN_ID, text)
            time.sleep(60)
        time.sleep(30)
            time.sleep(60)

        time.sleep(30)

threading.Thread(target=reminder).start()
threading.Thread(target=weekly_report).start()

bot.polling(none_stop=True)
