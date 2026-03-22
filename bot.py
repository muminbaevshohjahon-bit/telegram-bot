import telebot
import os
import random
import json # Ma'lumotlarni saqlash uchun
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# Ma'lumotlarni faylga saqlash funksiyalari (Restartdan himoya)
def save_data():
    with open('users_db.json', 'w') as f:
        json.dump(user_data, f)

def load_data():
    if os.path.exists('users_db.json'):
        with open('users_db.json', 'r') as f:
            return json.load(f)
    return {}

user_data = load_data()

DAILY_TASKS = [
    "Tongda detox (1 soat) 📵", "Kitob mutolasi 📚", "Sugar detox 🍬",
    "Gazsiz ichimliklar 🥤", "5000 so'm sarmoya 💰", "Jismoniy mashq 💪",
    "1 daqiqa hech narsa qilmaslik 🧘‍♂️"
]

MOTIVATIONS = [ # Qavs to'g'irlandi
    "Sen boshlamasang, hech narsa boshlanmaydi.", "Bugungi og‘riq — ertangi kuch.", 
    "Eng katta raqibing — kechagi o‘zing.", "G'alaba intizomni sevadi."
]

GIFS = [
    "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3eXJqM3Z4eXp5bmZ6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6JmR6PTEmZ3R6Z3R6/3o7TKDkDbIDJieKbVm/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOTVkZ3hueXBnNjkwZ2J1YjJkN2gwMHN3b3M3aXZ0cnRvMDFpbHdkZyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/FACfMgP1N9mlG/giphy.gif", # Vergul qo'yildi
    "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3eTZjbDQ0NjhqdmY5ZnJ5eDdqY2pvcHN2c21yMjZ3OHExcHdlanN0ayZlcD12MV9naWZzX3NlYXJjaCZjdD1n/XMnjfm65r82TirNhoe/giphy.gif"
]

def get_user(uid):
    uid = str(uid) # JSON kalitlari har doim string bo'ladi
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
        bot.send_message(uid, "Siz allaqachon ro'yxatdan o'tgansiz!", reply_markup=main_menu())
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

# Registratsiya handlerlari (O'zgarmadi, lekin save_data qo'shildi)
@bot.message_handler(func=lambda m: get_user(m.chat.id)['step'] == 'get_name')
def get_name(message):
    user = get_user(message.chat.id)
    user['info']['name'] = message.text
    user['step'] = 'get_birth'
    save_data()
    bot.send_message(message.chat.id, "Tug'ilgan yilingiz:")

@bot.message_handler(func=lambda m: get_user(message.chat.id)['step'] == 'get_nick')
def get_nick(message):
    user = get_user(message.chat.id)
    user['info']['nickname'] = message.text
    user['info']['reg_id'] = f"MBE-{random.randint(1000, 9999)}"
    user['step'] = 'main'
    save_data()
    bot.send_message(message.chat.id, f"Tayyor! ID: {user['info']['reg_id']}", reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == "Bugungi vazifalar ✅")
def show_tasks(message):
    uid = str(message.chat.id)
    user = get_user(uid)
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for task in DAILY_TASKS:
        # Bajarilgan vazifani belgilab ko'rsatish
        prefix = "✅ " if task in user.get('completed_today', []) else ""
        markup.add(KeyboardButton(f"{prefix}{task}"))
    markup.add(KeyboardButton("Orqaga ⬅️"))
    bot.send_message(uid, "Vazifalar:", reply_markup=markup)

@bot.message_handler(func=lambda m: any(task in m.text for task in DAILY_TASKS))
def handle_task(message):
    uid = str(message.chat.id)
    user = get_user(uid)
    task_name = message.text.replace("✅ ", "")
    
    if task_name not in user.get('completed_today', []):
        if 'completed_today' not in user: user['completed_today'] = []
        user['completed_today'].append(task_name)
        user['daily_count'] += 1
        user['total_score'] += 10
        save_data()
        bot.send_message(uid, f"Ajoyib! +10 ball. Bugun: {user['daily_count']}/7")
    else:
        bot.send_message(uid, "Bu vazifani bajarib bo'lgansiz! 😊")

@bot.message_handler(func=lambda m: m.text == "Finish 🏁")
def finish(message):
    uid = str(message.chat.id)
    user = get_user(uid)
    if user['daily_count'] == 0:
        bot.send_message(uid, "Hech bo'lmasa bitta ish qilaylik... 🙄")
        return

    percent = int((user['daily_count'] / 7) * 100)
    user['history'].append(f"{datetime.now().strftime('%d/%m')}: {percent}%")
    user['daily_count'] = 0
    user['completed_today'] = []
    save_data()
    
    motivation = random.choice(MOTIVATIONS)
    bot.send_animation(uid, random.choice(GIFS), caption=f"Natija: {percent}%\n\n{motivation}")

@bot.message_handler(func=lambda m: m.text == "Reyting 📊")
def ranking(message):
    # Faqat ro'yxatdan o'tganlarni saralash
    active_users = {k: v for k, v in user_data.items() if v['step'] == 'main'}
    sorted_u = sorted(active_users.items(), key=lambda x: x[1]['total_score'], reverse=True)[:10] # Top 10
    
    text = "🏆 TOP 10 FOYDALANUVCHI:\n\n"
    for i, (uid, data) in enumerate(sorted_u):
        text += f"{i+1}. {data['info']['nickname']} — {data['total_score']} ball\n"
    
    bot.send_message(message.chat.id, text)

bot.infinity_polling()
