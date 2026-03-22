import telebot
import os
import random
import json
import threading
import time
from datetime import datetime
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# --- DATA STORAGE ---
def load_data():
    if os.path.exists('users_db.json'):
        with open('users_db.json', 'r') as f:
            try: return json.load(f)
            except: return {}
    return {}

def save_data():
    with open('users_db.json', 'w') as f:
        json.dump(user_data, f)

user_data = load_data()

MOTIVATIONS = [
    "Sen boshlamasang, hech narsa boshlanmaydi.", "Bugungi og‘riq — ertangi kuch.",
    "Sen o‘ylagandan ham kuchlisan.", "Eng katta raqibing — kechagi o‘zing.",
    "Harakat — motivatsiyadan muhimroq.", "Vaqt ketmoqda — senchi?",
    "Intizom — erkinlik kaliti.", "Eng zo‘r vaqt — hozir."
]

GIFS = [
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaXU3bGl0dXg3c3FxM3VuZnl1ZW8wamRlbW5vbncxN2V1enNoNjhxOCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/8ZblO3ZD5NMltPaFS2/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaXU3bGl0dXg3c3FxM3VuZnl1ZW8wamRlbW5vbncxN2V1enNoNjhxOCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/g9582DNuQppxC/giphy.gif",
    "https://media.giphy.com/media/FACfMgP1N9mlG/giphy.gif"
]

def get_user(uid):
    uid = str(uid)
    if uid not in user_data:
        user_data[uid] = {'total_score': 0, 'history': [], 'completed_today': [], 'info': {}}
    return user_data[uid]

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    web_url = "https://muminbaevshohjahon-bit.github.io/telegram-bot/" # O'z linkizni tekshiring
    markup.add(KeyboardButton("Shaxsiy Kabinet 📱", web_app=WebAppInfo(url=web_url)))
    markup.add(KeyboardButton("Reyting 📊"), KeyboardButton("Natijalar jadvali 🏆"))
    markup.add(KeyboardButton("Finish 🏁"))
    return markup

# --- EVENTS ---
@bot.message_handler(commands=['start'])
def start(message):
    user = get_user(message.chat.id)
    bot.send_message(message.chat.id, "<b>Assalomu alaykum!</b>\n30 kunlik intizom chellenjiga xush kelibsiz!", parse_mode='HTML', reply_markup=main_menu())

@bot.message_handler(content_types=['web_app_data'])
def web_app_receive(message):
    data = json.loads(message.web_app_data.data)
    user = get_user(message.chat.id)
    
    # Agar bugun finish bosilgan bo'lsa, qabul qilmaslik
    today = datetime.now().strftime('%d/%m')
    if any(today in entry for entry in user['history']):
        bot.send_message(message.chat.id, "Bugun uchun vazifalar yakunlangan. Ertaga davom etamiz! ✨")
        return

    if data.get('action') == "done":
        task = data.get('task')
        user['total_score'] += 10
        user['completed_today'].append(task)
        save_data()
        
        bot.send_message(message.chat.id, f"✅ <b>{task}</b> bajarildi!\n\n{random.choice(MOTIVATIONS)}\n+10 ball!", parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "Finish 🏁")
def finish_day(message):
    user = get_user(message.chat.id)
    today = datetime.now().strftime('%d/%m')
    
    if any(today in entry for entry in user['history']):
        bot.send_message(message.chat.id, "Bugun allaqachon yakunlandi! 👋")
        return
    
    score = len(user['completed_today']) * 10
    user['history'].append(f"{today}: {score} ball")
    user['completed_today'] = []
    save_data()
    
    bot.send_animation(message.chat.id, random.choice(GIFS), caption=f"🏁 <b>Bugun yakunlandi!</b>\nTo'plangan ball: {score}\n\nErtaga ko'rishguncha!", parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "Reyting 📊")
def show_rank(message):
    sorted_u = sorted(user_data.items(), key=lambda x: x[1]['total_score'], reverse=True)[:10]
    text = "🏆 <b>TOP 10 ISHTIROKCHI</b>\n\n"
    for i, (uid, data) in enumerate(sorted_u):
        name = data.get('info', {}).get('nickname', f"Foydalanuvchi {uid[-3:]}")
        text += f"{i+1}. {name} — {data['total_score']} ball\n"
    bot.send_message(message.chat.id, text, parse_mode='HTML')

if __name__ == "__main__":
    bot.infinity_polling()
