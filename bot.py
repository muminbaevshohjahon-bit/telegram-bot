import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import sqlite3
from datetime import datetime
import threading
import time
import os

# SOZLAMALAR
TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
bot = telebot.TeleBot(TOKEN)

# BAZA BILAN ISHLASH
def get_db_connection():
    conn = sqlite3.connect("challenge.db", check_same_thread=False)
    return conn

conn = get_db_connection()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    full_name TEXT,
    birth_date TEXT, 
    nickname TEXT,
    points INTEGER DEFAULT 0
)
""")
conn.commit()

CHALLENGES = [
    "Gazsiz ichimliklar 🥤", "Tongda detox 📵", "Kitob mutolasi 📚", 
    "Sugar detox 🍬", "1 daqiqa tinchlik 🧘", "Badantarbiya 🏃", "Suv (6 bokal) 💧"
]

user_states = {}
user_tasks = {}

@bot.message_handler(commands=['start'])
def start(message):
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (message.from_user.id,))
    if cursor.fetchone():
        main_menu(message)
    else:
        bot.send_message(message.chat.id, "Assalomu alaykum! Ism-familiyangizni kiriting:")
        bot.register_next_step_handler(message, get_name)

def get_name(message):
    user_states[message.from_user.id] = {'full_name': message.text}
    bot.send_message(message.chat.id, "Tug'ilgan sanangizni kiriting (kun.oy.yil, masalan: 15.03.2004):")
    bot.register_next_step_handler(message, get_date)

def get_date(message):
    user_states[message.from_user.id]['birth_date'] = message.text
    bot.send_message(message.chat.id, "O'zingizga nickname (taxallus) tanlang:")
    bot.register_next_step_handler(message, get_nickname)

def get_nickname(message):
    uid = message.from_user.id
    nick = message.text
    data = user_states.get(uid)
    if data:
        cursor.execute("INSERT INTO users (user_id, full_name, birth_date, nickname) VALUES (?, ?, ?, ?)",
                       (uid, data['full_name'], data['birth_date'], nick))
        conn.commit()
        bot.send_message(message.chat.id, "Muvaffaqiyatli ro'yxatdan o'tdingiz! 🚀")
        main_menu(message)

def main_menu(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Bugungi vazifalar ✅"), KeyboardButton("Leaderboard 🏆"))
    bot.send_message(message.chat.id, "Asosiy menyu:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "Bugungi vazifalar ✅")
def show_tasks(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for t in CHALLENGES: markup.add(KeyboardButton(t))
    markup.add(KeyboardButton("Finish 🏁"))
    bot.send_message(message.chat.id, "Vazifalarni bajaring:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in CHALLENGES)
def complete(message):
    uid = message.from_user.id
    if uid not in user_tasks: user_tasks[uid] = set()
    user_tasks[uid].add(message.text)
    bot.send_message(message.chat.id, f"{message.text} bajarildi! ✅")

@bot.message_handler(func=lambda m: m.text == "Finish 🏁")
def finish(message):
    uid = message.from_user.id
    completed = len(user_tasks.get(uid, []))
    points_to_add = completed * 10
    
    # Quvib o'tish motivatsiyasi
    cursor.execute("SELECT nickname FROM users WHERE user_id != ? AND points > (SELECT points FROM users WHERE user_id = ?) ORDER BY points ASC LIMIT 1", (uid, uid))
    target = cursor.fetchone()

    cursor.execute("UPDATE users SET points = points + ? WHERE user_id = ?", (points_to_add, uid))
    conn.commit()
    
    msg = f"Bugun {points_to_add} ball to'pladingiz! 🔥"
    if target:
        msg += f"\n\nSizga {target[0]} dan o'tib ketishingizga oz qoldi! Bo'shashmang! 💪"

    bot.send_message(uid, msg)
    user_tasks[uid] = set()
    main_menu(message)

@bot.message_handler(func=lambda m: m.text == "Leaderboard 🏆")
def leaderboard(message):
    uid = message.from_user.id
    cursor.execute("SELECT user_id, nickname, points, full_name FROM users ORDER BY points DESC")
    users = cursor.fetchall()
    
    text = "🏆 LEADERBOARD:\n\n"
    for i, u in enumerate(users, 1):
        if uid == ADMIN_ID:
            # SIZ UCHUN: To'liq ismlar ko'rinadi
            text += f"{i}. {u[3]} (@{u[1]}) — {u[2]} ball\n"
        else:
            # QATNASHCHILAR UCHUN: Nickname va ID ko'rinadi
            text += f"{i}. {u[1]} (ID: {str(u[0])[:4]}***) — {u[2]} ball\n"
    
    bot.send_message(message.chat.id, text)

# Eslatmalar
def scheduler():
    while True:
        t = datetime.now().strftime("%H:%M")
        if t in ["07:00", "13:00", "21:00"]:
            cursor.execute("SELECT user_id FROM users")
            for r in cursor.fetchall():
                try: bot.send_message(r[0], "Vazifalarni bajarishni unutmang! 🚀")
                except: pass
            time.sleep(60)
        time.sleep(30)

threading.Thread(target=scheduler, daemon=True).start()
bot.polling(none_stop=True)
