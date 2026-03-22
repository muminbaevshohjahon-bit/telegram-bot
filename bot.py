import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import sqlite3
from datetime import datetime
import threading
import time
import os

# Sozlamalar
TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
bot = telebot.TeleBot(TOKEN)

# Ma'lumotlar bazasi
conn = sqlite3.connect("challenge.db", check_same_thread=False)
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
    bot.send_message(message.chat.id, "Tug'ilgan sanangizni kiriting (kun.oy.yil, masalan: 15.05.2004):")
    bot.register_next_step_handler(message, get_date)

def get_date(message):
    user_states[message.from_user.id]['birth_date'] = message.text
    bot.send_message(message.chat.id, "O'zingizga nickname (taxallus) tanlang:")
    bot.register_next_step_handler(message, get_nickname)

def get_nickname(message):
    uid = message.from_user.id
    nick = message.text
    data = user_states[uid]
    cursor.execute("INSERT INTO users (user_id, full_name, birth_date, nickname) VALUES (?, ?, ?, ?)",
                   (uid, data['full_name'], data['birth_date'], nick))
    conn.commit()
    bot.send_message(message.chat.id, "Tabriklaymiz! Muvaffaqiyatli ro'yxatdan o'tdingiz! 🚀")
    main_menu(message)

def main_menu(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Bugungi vazifalar ✅"))
    markup.add(KeyboardButton("Leaderboard 🏆"))
    bot.send_message(message.chat.id, "Asosiy menyu:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "Bugungi vazifalar ✅")
def show_tasks(message):
    if datetime.now().hour >= 23:
        bot.send_message(message.chat.id, "Bugun uchun qabul yopilgan (23:00).")
        return
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
    
    # Quvib o'tishni tekshirish (Ball qo'shishdan oldin kimdan o'tayotganini ko'rish)
    cursor.execute("SELECT nickname, points FROM users WHERE user_id != ? AND points > ? ORDER BY points ASC LIMIT 1", 
                   (uid, points_to_add))
    target = cursor.fetchone()

    cursor.execute("UPDATE users SET points = points + ? WHERE user_id = ?", (points_to_add, uid))
    conn.commit()
    
    # Motivatsiya yuborish
    if target:
        bot.send_message(uid, f"🔥 Zo'r! Siz
