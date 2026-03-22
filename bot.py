import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import sqlite3
from datetime import datetime
import threading
import time
import os

# Sozlamalar
TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0")) # Sizning ID raqamingiz
bot = telebot.TeleBot(TOKEN)

# Ma'lumotlar bazasini sozlash
conn = sqlite3.connect("challenge.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    full_name TEXT,
    birth_year TEXT,
    nickname TEXT,
    points INTEGER DEFAULT 0,
    streak INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS daily_stats (
    user_id INTEGER,
    date TEXT,
    tasks_completed INTEGER,
    total_tasks INTEGER,
    PRIMARY KEY (user_id, date)
)
""")
conn.commit()

CHALLENGES = [
    "Gazsiz ichimliklar 🥤",
    "Tongda detox (1 soat) 📵",
    "Kitob mutolasi 📚",
    "Sugar detox 🍬",
    "1 daqiqa tinchlik 🧘",
    "Badantarbiya 🏃",
    "Suv (6 bokal) 💧"
]

user_data = {}

# --- RO'YXATDAN O'TISH QISMI ---

@bot.message_handler(commands=['start'])
def start(message):
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (message.from_user.id,))
    user = cursor.fetchone()
    if user:
        main_menu(message)
    else:
        bot.send_message(message.chat.id, "Assalomu alaykum! Challenge botiga xush kelibsiz. Ismingizni kiriting:")
        bot.register_next_step_handler(message, get_name)

def get_name(message):
    user_data[message.from_user.id] = {'full_name': message.text}
    bot.send_message(message.chat.id, "Tug'ilgan yilingizni kiriting (masalan: 2004):")
    bot.register_next_step_handler(message, get_year)

def get_year(message):
    user_data[message.from_user.id]['year'] = message.text
    bot.send_message(message.chat.id, "O'zingiz uchun nickname (taxallus) oling:")
    bot.register_next_step_handler(message, get_nickname)

def get_nickname(message):
    nick = message.text
    data = user_data[message.from_user.id]
    cursor.execute("INSERT INTO users (user_id, full_name, birth_year, nickname) VALUES (?, ?, ?, ?)",
                   (message.from_user.id, data['full_name'], data['year'], nick))
    conn.commit()
    
    bot.send_message(message.chat.id, "Tabriklaymiz, muvaffaqiyatli ro'yxatdan o'tdingiz! Challenge boshlandi! 🚀")
    main_menu(message)

# --- ASOSIY MENU ---

def main_menu(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Bugungi vazifalar ✅"))
    markup.add(KeyboardButton("Leaderboard 🏆"), KeyboardButton("Statistika 📊"))
    bot.send_message(message.chat.id, "Asosiy menyu:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "Bugungi vazifalar ✅")
def show_tasks(message):
    now = datetime.now()
    if now.hour >= 23:
        bot.send_message(message.chat.id, "Bugun uchun qabul vaqti tugadi (23:00 gacha edi).")
        return

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for task in CHALLENGES:
        markup.add(KeyboardButton(task))
    markup.add(KeyboardButton("Finish 🏁"))
    bot.send_message(message.chat.id, "Vazifalarni bajargach belgilang:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in CHALLENGES)
def complete_task(message):
    uid = message.from_user.id
    task = message.text
    
    if uid not in user_data: user_data[uid] = set()
    user_data[uid].add(task)
    
    # Kayfiyat uchun rasm (ixtiyoriy rasm linki)
    bot.send_photo(message.chat.id, "https://api.dicebear.com/7.x/thumbs/png?seed=" + task, 
                   caption=f"Ajoyib! {task} bajarildi ✅")

@bot.message_handler(func=lambda m: m.text == "Finish 🏁")
def finish_day(message):
    uid = message.from_user.id
    completed = len(user_data.get(uid, []))
    total = len(CHALLENGES)
    percent = int((completed / total) * 100)
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("INSERT OR REPLACE INTO daily_stats VALUES (?, ?, ?, ?)", (uid, date_str, completed, total))
    
    # Ballarni yangilash
    cursor.execute("UPDATE users SET points = points + ? WHERE user_id = ?", (completed * 10, uid))
    conn.commit()

    if percent == 100:
        msg = f"🔥 100% bajarildi!\nSen intizomli insonlar safidasan! Sen bilan faxrlanamiz! 🌟"
    else:
        msg = f"📊 {percent}% bajarildi.\nSenga ishonamiz! Bundan ko'prog'iga loyiqsan! 💪"
    
    bot.send_message(message.chat.id, msg)
    user_data[uid] = set() # Tozalash
    main_menu(message)

# --- LEADERBOARD ---

@bot.message_handler(func=lambda m: m.text == "Leaderboard 🏆")
def leaderboard(message):
    cursor.execute("SELECT nickname, points FROM users ORDER BY points DESC LIMIT 10")
    top_users = cursor.fetchall()
    
    text = "🏆 TOP FOYDALANUVCHILAR:\n\n"
    for i, user in enumerate(top_users, 1):
        text += f"{i}. {user[0]} — {user[1]} ball\n"
    
    bot.send_message(message.chat.id, text)

# --- AVTOMATIK ESLATMALAR ---

def scheduler():
    while True:
        now = datetime.now().strftime("%H:%M")
        
        # Tonggi eslatma
        if now == "07:00":
            send_to_all("☀️ Tongda: Bugun sen ko'prog'iga qodirsan!\nQani bo'l bo'shashma!")
        
        # Tushlik
        elif now == "13:00":
            send_to_all("🥗 Tushlik vaqti: Chellenjlar seni kutayabdi!")
            
        # Kechki
        elif now == "20:00":
            send_to_all("🌙 Kechqurun: Oz qoldi! Senga ishonamiz!")
            
        time.sleep(60)

def send_to_all(text):
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()
    for user in users:
        try:
            bot.send_message(user[0], text)
        except:
            pass

# Threadni ishga tushirish
threading.Thread(target=scheduler, daemon=True).start()

bot.polling(none_stop=True)
