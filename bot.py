import telebot
import os
import random
import threading
import time
import json
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# --- DATA PERSISTENCE ---
def save_data():
    with open('users_db.json', 'w') as f:
        json.dump(user_data, f)

def load_data():
    if os.path.exists('users_db.json'):
        with open('users_db.json', 'r') as f:
            try: return json.load(f)
            except: return {}
    return {}

user_data = load_data()

DAILY_TASKS = [
    "Tongda detox (1 soat) 📵", "Kitob mutolasi 📚", "Sugar detox 🍬",
    "Gazsiz ichimliklar 🥤", "5000 so'm sarmoya 💰", "Jismoniy mashq 💪",
    "1 daqiqa hech narsa qilmaslik 🧘‍♂️"
]

MOTIVATIONS = [
    "Sen boshlamasang, hech narsa boshlanmaydi.", "Bugungi og‘riq — ertangi kuch.",
    "Har kuni kichik qadam — katta natija.", "Eng yaxshi vaqt — hozir.",
    "Intizom — erkinlik kaliti.", "O‘z ustingda ishlash — eng yaxshi investitsiya.","Og‘riq vaqtinchalik — natija abadiy.", "Bugungi mehnat — ertangi faxr.",
    "Sen o‘zingni o‘zgartirsang, hayoting o‘zgaradi.", "Kuchli bo‘lish — tanlov.",
    "Intizom — erkinlik kaliti.", "Qachon qiyin bo‘lsa — o‘sha payt o‘sasan.",
    "Orqaga emas, oldinga qaragin.", "Hech kim mukammal emas — lekin harakat qilayotganlar yutadi.",
    "O‘z ustingda ishlash — eng yaxshi investitsiya.", "Sen bunga qodirsan.",
    "Kech emas — hali vaqt bor.", "Boshlash — yarim g‘alaba.",
    "Kuchli odamlar bahona qilmaydi.", "Har kuni yangi imkoniyat.",
    "Sen taslim bo‘lsang — hammasi tugaydi.", "Sen davom etsang — hammasi boshlanadi.",
    "O‘z yo‘lingni o‘zing yarat.", "Orzularing seni chaqiryapti.",
    "Qadam tashla — yo‘l ochiladi.", "O‘zinga ishongan odam yutadi.",
    "Harakat qil, hatto sekin bo‘lsa ham.", "Katta natija — kichik odatlardan boshlanadi.",
    "Sabrsizlar yutqazadi.", "Qiyinchilik — vaqtinchalik mehmon.",
    "Sen o‘zingni kashf qilmagansan hali.", "Har kuni o‘z ustingda ishlagin.",
    "Yutuq — chidamlilik mevasidir.", "Sen o‘zingni cheklayapsan.",
    "O‘zingga imkon ber.", "Eng katta tavakkal — urinmaslik.",
    "Qo‘rquv seni to‘xtatmasin.", "Sen o‘zingni o‘zgartira olasan.",
    "Bugun boshlagan odam ertaga yutadi.", "Hech qachon kech emas.",
    "Harakat qil — natija keladi.", "Sen kuchsiz emassan — charchagansan xolos.",
    "Dam ol, lekin taslim bo‘lma.", "Har kuni 1% yaxshilan.",
    "Qanchalik qiynalsang, shunchalik qadrlaysan.", "Sen bunga arziysan.",
    "O‘z hayotingni o‘zgartir.", "Yutuq oson kelmaydi.",
    "Harakat qilmaslik — eng katta xato.", "Sen o‘zingni sinab ko‘r.",
    "Orzular — jasurlarga tegishli.", "Sen hali imkoniyatlaringni ishlatmading.",
    "O‘zingga sodiq bo‘l.", "Qiyin yo‘l — to‘g‘ri yo‘l bo‘lishi mumkin.",
    "Taslim bo‘lish — variant emas.", "Sen yutishga yaratilgansan.",
    "Harakat qil — sharoit o‘zgaradi.", "Sen boshlagan ishni tugat.",
    "Eng zo‘r vaqt — hozir.", "O‘zgarish sendan boshlanadi.",
    "Sen kuchli bo‘lishni tanla.", "O‘zingni o‘zing motivatsiya qil.",
    "Har kuni yangi imkon.", "Sen hali eng yaxshisini ko‘rmading.",
    "O‘z yo‘lingni tanla va yur.", "Sen bunga qodirsan — ishon.",
    "Harakat qilgan odam yutadi.", "Qanchalik qiyin bo‘lsa — shunchalik qiymatli.",
    "Sen hech qachon yolg‘iz emassan — o‘zing bor.", "Boshlagin. Hozir. Shu yerda."
]

GIFS = [
    "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3eXJqM3Z4eXp5bmZ6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6JmR6PTEmZ3R6Z3R6/3o7TKDkDbIDJieKbVm/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOTVkZ3hueXBnNjkwZ2J1YjJkN2gwMHN3b3M3aXZ0cnRvMDFpbHdkZyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/FACfMgP1N9mlG/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3eTZjbDQ0NjhqdmY5ZnJ5eDdqY2pvcHN2c21yMjZ3OHExcHdlanN0ayZlcD12MV9naWZzX3NlYXJjaCZjdD1n/XMnjfm65r82TirNhoe/giphy.gif"
]

# --- HELPERS ---
def get_user(uid):
    uid = str(uid)
    if uid not in user_data:
        user_data[uid] = {
            'info': {}, 'daily_count': 0, 'history': [],
            'total_score': 0, 'completed_tasks': [], 'step': 'start'
        }
    return user_data[uid]

def main_menu():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(KeyboardButton("Bugungi vazifalar ✅"), KeyboardButton("Natijalar jadvali 🏆"))
    markup.add(KeyboardButton("Reyting 📊"), KeyboardButton("Finish 🏁"))
    return markup

# --- REGISTRATION (YANGILANDI) ---

@bot.message_handler(commands=['start'])
def start(message):
    uid = str(message.chat.id)
    user = get_user(uid)
    
    # Start xabari
    welcome_text = (
        "Assalomu aleykum botimizga hush kelibsiz! "
        "Bu yerda 30 kunlik chellenge bo'ladi bot MBE useful tomonidna yaratilgan! "
        "foydasi tegsa hursandmiz.\n\n"
        "<b>Keling tanishib olaylik... Ismingizni kiriting:</b>"
    )
    user['step'] = 'get_name'
    save_data()
    bot.send_message(uid, welcome_text, parse_mode='HTML')

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_name')
def get_name(message):
    user = get_user(message.chat.id)
    user['info']['name'] = message.text
    user['step'] = 'get_birth'
    save_data()
    bot.send_message(message.chat.id, "Tug‘ilgan yilingiz (masalan, 2003):")

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_birth')
def get_birth(message):
    user = get_user(message.chat.id)
    user['info']['birth_year'] = message.text
    user['step'] = 'get_month'
    save_data()
    bot.send_message(message.chat.id, "Tug‘ilgan oyingiz (1-12):")

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_month')
def get_month(message):
    user = get_user(message.chat.id)
    user['info']['birth_month'] = message.text
    user['step'] = 'get_day'
    save_data()
    bot.send_message(message.chat.id, "Tug‘ilgan kuningiz (1-31):")

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_day')
def get_day(message):
    user = get_user(message.chat.id)
    user['info']['birth_day'] = message.text
    user['step'] = 'get_nick'
    save_data()
    bot.send_message(message.chat.id, "Nickname tanlang (masalan, Sichqon):")

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_nick')
def get_nick(message):
    user = get_user(message.chat.id)
    user['info']['nickname'] = message.text
    user['step'] = 'main'
    
    # ID yaratish
    public_id = f"ID_{random.randint(1000, 9999)}"
    user['info']['public_id'] = public_id
    
    save_data()
    bot.send_message(
        message.chat.id, 
        f"Ro‘yxatdan o‘tdingiz! Sizning identifikatoringiz: <b>({public_id} {message.text})</b>", 
        parse_mode='HTML', 
        reply_markup=main_menu()
    )

# --- REYTING (FORMAT O'ZGARTIRILDI) ---

@bot.message_handler(func=lambda m: m.text == "Reyting 📊")
def show_rank(message):
    # Ballar bo'yicha saralash
    active_users = [u for u in user_data.values() if u.get('step') == 'main']
    sorted_u = sorted(active_users, key=lambda x: x['total_score'], reverse=True)[:10]
    
    text = "🏆 <b>TOP 10 REYTING</b>\n\n"
    for i, data in enumerate(sorted_u):
        p_id = data['info'].get('public_id', 'ID_0000')
        nick = data['info'].get('nickname', 'User')
        score = data['total_score']
        text += f"{i+1}. ({p_id} {nick}) — {score} ball\n"
    
    bot.send_message(message.chat.id, text, parse_mode='HTML')

# --- QOLGAN FUNKSIYALAR (Finish, Tasks va h.k.) ---
# ... (O'zgarishsiz qoladi)

@bot.message_handler(func=lambda m: m.text == "Finish 🏁")
def finish_day(message):
    user = get_user(message.chat.id)
    if user['daily_count'] == 0:
        bot.send_message(message.chat.id, "Hech bo'lmasa bitta vazifa bajaring!")
        return
    percent = int((user['daily_count'] / len(DAILY_TASKS)) * 100)
    user['history'].append(f"{datetime.now().strftime('%d/%m')} - {percent}%")
    bot.send_animation(message.chat.id, random.choice(GIFS), caption=f"🏁 Natija: {percent}%\n\n{random.choice(MOTIVATIONS)}")
    user['daily_count'] = 0
    user['completed_tasks'] = []
    save_data()

# --- POLLING ---
bot.infinity_polling()
