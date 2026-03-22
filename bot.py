import telebot
import os
import random
import json
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# Ma'lumotlarni faylga saqlash (Restartdan himoya)
def save_data():
    with open('users_db.json', 'w') as f:
        json.dump(user_data, f)

def load_data():
    if os.path.exists('users_db.json'):
        with open('users_db.json', 'r') as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

user_data = load_data()

DAILY_TASKS = [
    "Tongda detox (1 soat) 📵", "Kitob mutolasi 📚", "Sugar detox 🍬",
    "Gazsiz ichimliklar 🥤", "5000 so'm sarmoya 💰", "Jismoniy mashq 💪",
    "1 daqiqa hech narsa qilmaslik 🧘‍♂️"
]

MOTIVATIONS = [
    "Sen boshlamasang, hech narsa boshlanmaydi.", "Bugungi og‘riq — ertangi kuch.", 
    "Eng katta raqibing — kechagi o‘zing.", "G'alaba intizomni sevadi."
]

GIFS = [
    "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3eXJqM3Z4eXp5bmZ6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6JmR6PTEmZ3R6Z3R6/3o7TKDkDbIDJieKbVm/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOTVkZ3hueXBnNjkwZ2J1YjJkN2gwMHN3b3M3aXZ0cnRvMDFpbHdkZyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/FACfMgP1N9mlG/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3eTZjbDQ0NjhqdmY5ZnJ5eDdqY2pvcHN2c21yMjZ3OHExcHdlanN0ayZlcD12MV9naWZzX3NlYXJjaCZjdD1n/XMnjfm65r82TirNhoe/giphy.gif"
]

def get_user(uid):
    uid = str(uid)
    if uid not in user_data:
        user_data[uid] = {
            'info': {}, 'daily_count': 0, 'history': [], 
            'total_score': 0, 'step': 'start', 'completed_today': []
        }
    return user_data[uid]

def main_menu():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(KeyboardButton("Bugungi vazifalar ✅"), KeyboardButton("Natijalar jadvali 🏆"))
    markup.add(KeyboardButton("Reyting 📊"), KeyboardButton("Finish 🏁"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    uid = str(message.chat.id)
    user = get_user(uid)
    
    if user['step'] == 'main':
        bot.send_message(uid, "Xush kelibsiz! Vazifalarni davom ettiramiz.", reply_markup=main_menu())
        return

    welcome_text = (
        "<b>Assalomu aleykum!</b>\n"
        "30-kunlik chellenj botiga xush kelibsiz!\n\n"
        "<i>Bot MBE useful tomonidan yaratilgan.</i>\n\n"
        "Keling, tanishib olaylik! <b>Ismingizni kiriting:</b>"
    )
    user['step'] = 'get_name'
    save_data()
    bot.send_message(uid, welcome_text, parse_mode='HTML')

# --- RO'YXATDAN O'TISH BOSQICHLARI (Xatolar to'g'irlandi) ---

@bot.message_handler(func=lambda m: get_user(m.chat.id)['step'] == 'get_name')
def get_name(message):
    user = get_user(message.chat.id)
    user['info']['name'] = message.text
    user['step'] = 'get_birth'
    save_data()
    bot.send_message(message.chat.id, "Tug'ilgan yilingizni kiriting:")

@bot.message_handler(func=lambda m: get_user(m.chat.id)['step'] == 'get_birth')
def get_birth(message):
    user = get_user(message.chat.id)
    user['info']['birth_year'] = message.text
    user['step'] = 'get_nick' # Endi nickname'ga o'tadi
    save_data()
    bot.send_message(message.chat.id, "O'zingizga nickname tanlang :)")

@bot.message_handler(func=lambda m: get_user(m.chat.id)['step'] == 'get_nick')
def get_nick(message):
    user = get_user(message.chat.id)
    user['info']['nickname'] = message.text
    user['info']['reg_id'] = f"MBE-{random.randint(1000, 9999)}"
    user['step'] = 'main'
    save_data()
    bot.send_message(message.chat.id, f"Tayyor! Sizning ID raqamingiz: <b>{user['info']['reg_id']}</b>", parse_mode='HTML', reply_markup=main_menu())

# --- ASOS
