import telebot
import os
import random
import json
import threading
import time
from datetime import datetime
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

# Vaqt zonasi
os.environ['TZ'] = 'Asia/Tashkent'
if hasattr(time, 'tzset'):
    time.tzset()

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# --- KONFIGURATSIYA ---
ADMIN_ID = 6338204692 
CHANNELS = ["@mbe_useful"] 
TOTAL_TASKS = 8 # 7 ta odatiy + 1 ta uyqu vazifasi

# --- MA'LUMOTLAR BILAN ISHLASH ---
def load_data():
    try:
        with open('users_db.json', 'r') as f:
            return json.load(f)
    except:
        return {}

def save_data():
    with open('users_db.json', 'w') as f:
        json.dump(user_data, f, indent=4)

user_data = load_data()

# MOTIVATSIYALAR
CUSTOM_MOTIVATIONS = [
    "Sen boshlamasang, hech narsa boshlanmaydi. 🔥", "Bugungi og‘riq — ertangi kuch. 💪",
    "Eng zo‘r vaqt — hozir. 🚀", "Intizom — bu o'ziga berilgan va'dani bajarishdir. ✨",
    "Har kuni kichik qadam — katta natija.", "Eng katta raqibing — kechagi o‘zing.",
    "Mukammallikni kutma — harakatni boshlash muhim.", "Sen o‘ylagandan ham kuchlisan.",
    "Hech kim seni qutqarmaydi — o‘zingni o‘zing ko‘tar.", "Qiyinchilik — bu yashirin imkoniyat.",
    "Orzular faqat harakat bilan haqiqatga aylanadi.", "Qo‘rqish — o‘sish boshlanishidir.",
    "Sen taslim bo‘lmaguningcha, yutqazmading.", "Bahonalar seni orqaga tortadi.",
    "Harakat — motivatsiyadan muhimroq.", "Vaqt ketmoqda — senchi?",
    "O‘zgarish og‘riqli, lekin zarur.", "Natija sabrni yaxshi ko‘radi.",
    "Bugun qilmaganing — ertaga pushaymon bo‘ladi.", "Kichik boshlashdan uyalmagin.",
    "Eng katta tavakkal — urinmaslik.", "Qo‘rquv seni to‘xtatmasin.",
    "O‘zingga sodiq bo‘l.", "Taslim bo‘lish — variant emas.",
    "O‘zgarish sendan boshlanadi.", "Boshlagin. Hozir. Shu yerda.",
    "Aqilli inson uchun har kuni yangi kun boshlanadi.","Kuchsizlar faqat taslim bo'ladi."
]

FINISH_MOTIVATIONS = [
    "Dahshat! Vapshe zo'r, barakalla! 🔥",
    "Sen o'ylagandan ham kuchlisan, davom et! 💪",
    "Intizom — bu o'zingga bo'lgan hurmat. 🌟",
    "Bo'lar ekanku, senga ishonaman!",
    "Bo'shashma zo'r ketayabsan",
    "Ko'zim to'rt bo'lib ketdi, malades."
]


GIFS = [
   "https://media.giphy.com/media/FACfMgP1N9mlG/giphy.gif",
   "https://media2.giphy.com/media/fUQ4rhUZJYiQsas6WD/giphy.gif",
   "https://media.giphy.com/media/tHIRLHtNwxpjIFqPdV/giphy.gif",
   "https://media.giphy.com/media/8ZblO3ZD5NMltPaFS2/giphy.gif"
]

# --- YORDAMCHI FUNKSIYALAR ---
def check_sub(uid):
    """Obunani qat'iy tekshirish"""
    for channel in CHANNELS:
        try:
            status = bot.get_chat_member(channel, uid).status
            if status in ['left', 'kicked']:
                return False
        except Exception:
            continue 
    return True

def get_user(uid):
    uid = str(uid)
    if uid not in user_data:
        user_data[uid] = {'total_score': 0, 'history': [], 'completed_today': [], 'info': {}, 'step': 'start'}
    return user_data[uid]

def main_menu(uid):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    web_url = f"https://muminbaevshohjahon-bit.github.io/telegram-bot/?v={random.randint(1, 999999)}"
    markup.add(KeyboardButton("Chellenjlar🗓", web_app=WebAppInfo(url=web_url)))
    markup.add(KeyboardButton("Peshqadamlar 🏆"), KeyboardButton("Mening natijam 📊"))
    markup.add(KeyboardButton("Finish 🏁"))
    if int(uid) == ADMIN_ID:
        markup.add(KeyboardButton("/admin 👨‍💻"))
    return markup

# --- START VA REGISTRATSIYA ---
@bot.message_handler(commands=['start'])
def start(message):
    uid = message.chat.id
    if not check_sub(uid):
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Kanalga a'zo bo'lish 📢", url=f"https://t.me/{CHANNELS[0].replace('@', '')}"))
        bot.send_message(uid, "<b>Botdan foydalanish uchun kanalimizga a'zo bo'ling!</b>", parse_mode='HTML', reply_markup=markup)
        return

    user = get_user(uid)
    if user.get('info', {}).get('name'):
        bot.send_message(uid, "Xush kelibsiz! Vazifalarni bajarishda davom eting.", reply_markup=main_menu(uid))
        return

    user_data[str(uid)]['step'] = 'get_name'
    save_data()
    
    welcome_text = (
        "<b><i>Assalomu aleykum xush kelibsiz!</i></b>\n"
        "<b><i>Men MBE useful tomonidan yaratilgan botman!</i></b>\n\n"
        "<b><i>Maqsadimiz 30 kunlik chellenj davomida intizomni shakllantirish.</i></b>\n\n"
        "Keling tanishib olaylik... Ismingizni kiriting:"
    )
    bot.send_message(uid, welcome_text, parse_mode='HTML')

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_name')
def get_name(message):
    uid = str(message.chat.id)
    user_data[uid]['info']['name'] = message.text
    user_data[uid]['step'] = 'get_year'
    save_data()
    bot.send_message(uid, "Tug‘ilgan yilingiz:")

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_year')
def get_year(message):
    uid = str(message.chat.id)
    user_data[uid]['info']['birth_year'] = message.text
    user_data[uid]['step'] = 'get_nick'
    save_data()
    bot.send_message(uid, "Nickname kiriting:")

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_nick')
def get_nick(message):
    uid = str(message.chat.id)
    user_data[uid]['info']['nickname'] = message.text
    user_data[uid]['step'] = 'main'
    save_data()
    bot.send_message(uid, "Tabrikleymiz, ro'yxatdan o'tildi!🔥", reply_markup=main_menu(uid))

# --- PESHQADAMLAR ---
@bot.message_handler(func=lambda m: m.text == "Peshqadamlar 🏆")
def leaderboard(message):
    if not check_sub(message.chat.id): return
    
    sorted_users = sorted(
        user_data.items(), 
        key=lambda x: x[1].get('total_score', 0), 
        reverse=True
    )
    
    leader_text = "🏆 <b>Eng kuchli intizom egalari:</b>\n\n"
    
    for i, (uid, data) in enumerate(sorted_users[:10], 1):
        name = data.get('info', {}).get('name', "Foydalanuvchi")
        score = data.get('total_score', 0)
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        leader_text += f"{medal} <b>{name}</b> — {score} ball\n"
    
    if not sorted_users:
        leader_text += "Hozircha natijalar yo'q."
        
    bot.send_message(message.chat.id, leader_text, parse_mode='HTML')

# --- NATIJALAR VA FINISH ---
@bot.message_handler(func=lambda m: m.text == "Mening natijam 📊")
def my_stats(message):
    if not check_sub(message.chat.id): return
    user = get_user(message.chat.id)
    history = user.get('history', [])
    stat_text = "📊 <b>Haftalik natijalar:</b>\n\n"
    if not history: 
        stat_text += "Hali natija yo'q."
    else:
        for entry in history[-7:]:
            try:
                day, res = entry.split(": ")
                p_val = int(res.replace('%', ''))
                bar = "🟦" * (p_val // 10) + "⬜️" * (10 - (p_val // 10))
                stat_text += f"<code>{day}</code> {bar} <b>{p_val}%</b>\n"
            except: continue
    stat_text += f"\n🔥 Umumiy ball: {user.get('total_score', 0)}"
    bot.send_message(message.chat.id, stat_text, parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "Finish 🏁")
def finish_day(message):
    if not check_sub(message.chat.id): return
    uid = str(message.chat.id)
    user = get_user(uid)
    today = datetime.now().strftime('%d/%m')
    
    if any(today in entry for entry in user.get('history', [])):
        bot.send_message(uid, "Bugun yakunlab bo'lingan! ✨")
        return
    
    percent = int((len(user.get('completed_today', [])) / TOTAL_TASKS) * 100)
    user.setdefault('history', []).append(f"{today}: {percent}%")
    user['completed_today'] = []
    save_data()
    
    bot.send_message(uid, f"🏁 Kunlik natija: {percent}% saqlandi!")

# --- ADMIN PANEL ---
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.chat.id == ADMIN_ID:
        bot.send_message(message.chat.id, f"👥 Jami foydalanuvchilar: {len(user_data)}\n/db_download - Bazani yuklash")

@bot.message_handler(commands=['db_download'])
def db_download(message):
    if message.chat.id == ADMIN_ID:
        try:
            with open('users_db.json', 'rb') as f:
                bot.send_document(message.chat.id, f)
        except:
            bot.send_message(message.chat.id, "Fayl topilmadi.")

if __name__ == "__main__":
    bot.infinity_polling()
