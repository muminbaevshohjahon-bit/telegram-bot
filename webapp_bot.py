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

# --- SOZLAMALAR ---
ADMIN_ID = 6338204692 
CHANNELS = ["@mbe_useful"] # O'z kanalingizni kiriting
TOTAL_TASKS = 8 # 7 ta odatiy + 1 ta uyqu vazifasi

# --- MA'LUMOTLAR ---
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
    "Hech kim seni qutqarmaydi — o‘zingni o‘zing ko‘tar.💪", "Qiyinchilik — bu yashirin imkoniyat.",
    "Orzular faqat harakat bilan haqiqatga aylanadi.", "Qo‘rqish — o‘sish boshlanishidir.",
    "Sen taslim bo‘lmaguningcha, yutqazmading.", "Bahonalar seni orqaga tortadi.",
    "Harakat — motivatsiyadan muhimroq.", "Vaqt ketmoqda — senchi?",
    "O‘zgarish og‘riqli, lekin zarur.🔥", "Natija sabrni yaxshi ko‘radi.",
    "Bugun qilmaganing — ertaga pushaymon bo‘ladi.", "Kichik boshlashdan uyalmagin.",
    "Eng katta tavakkal — urinmaslik.", "Qo‘rquv seni to‘xtatmasin.💪",
    "O‘zingga sodiq bo‘l.🔥", "Taslim bo‘lish — variant emas.💪",
    "O‘zgarish sendan boshlanadi.", "Boshlagin. Hozir. Shu yerda.",
    "Aqilli inson uchun har kuni yangi kun boshlanadi.","Kuchsizlar faqat taslim bo'ladi.🔥"
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
   "https://media.giphy.com/media/g9582DNuQppxC/giphy.gif"
]

# --- FUNKSIYALAR ---
def check_sub(user_id):
    for channel in CHANNELS:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status == 'left':
                return False
        except:
            return True 
    return True

def sub_markup():
    markup = InlineKeyboardMarkup()
    for channel in CHANNELS:
        markup.add(InlineKeyboardButton("Kanalga a'zo bo'lish 📢", url=f"https://t.me/{channel[1:]}"))
    markup.add(InlineKeyboardButton("Tekshirish ✅", callback_data="check_subscription"))
    return markup

def get_user(uid):
    uid = str(uid)
    if uid not in user_data:
        user_data[uid] = {'total_score': 0, 'history': [], 'completed_today': [], 'info': {}, 'step': 'start'}
    return user_data[uid]

def main_menu(user_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    web_url = f"https://muminbaevshohjahon-bit.github.io/telegram-bot/?v={random.randint(1, 999999)}"
    markup.add(KeyboardButton("Chellenjlar 🗓", web_app=WebAppInfo(url=web_url)))
    markup.add(KeyboardButton("Peshqadamlar 🏆"), KeyboardButton("Mening natijam 📊"))
    markup.add(KeyboardButton("Finish 🏁"))
    if user_id == ADMIN_ID:
        markup.add(KeyboardButton("/admin 👨‍💻"))
    return markup

# --- HANDLERLAR ---
@bot.message_handler(commands=['start'])
def start(message):
    uid = str(message.chat.id)
    if not check_sub(message.chat.id):
        bot.send_message(uid, "<b>Botdan foydalanish uchun kanalimizga a'zo bo'ling!</b>", 
                         parse_mode='HTML', reply_markup=sub_markup())
        return

    user_data[uid] = {'total_score': 0, 'history': [], 'completed_today': [], 'info': {}, 'step': 'get_name'}
    save_data()
    welcome_text = "<b>Assalomu aleykum!</b>\nKeling tanishib olaylik. Ismingizni kiriting:"
    bot.send_message(uid, welcome_text, parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data == "check_subscription")
def check_callback(call):
    if check_sub(call.from_user.id):
        bot.answer_callback_query(call.id, "Rahmat!")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        start(call.message)
    else:
        bot.answer_callback_query(call.id, "Siz hali a'zo bo'lmadingiz!", show_alert=True)

# --- REGISTRATSIYA ---
@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_name')
def get_name(message):
    uid = str(message.chat.id)
    user_data[uid]['info']['name'] = message.text
    user_data[uid]['step'] = 'get_year'
    save_data()
    bot.send_message(uid, "Tug‘ilgan yilingiz (masalan: 2004):")

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
    bot.send_message(uid, "Ro'yxatdan o'tildi!🔥", reply_markup=main_menu(message.chat.id))

# --- NATIJA VA GISTOGRAMMA ---
@bot.message_handler(func=lambda m: m.text == "Mening natijam 📊")
def my_stats(message):
    user = get_user(message.chat.id)
    history = user.get('history', [])
    stat_text = "📊 <b>Oxirgi 7 kunlik natijalar:</b>\n\n"
    
    if not history:
        stat_text += "Hali natija yo'q."
    else:
        for entry in history[-7:]:
            try:
                day, res = entry.split(": ")
                val = int(res.replace('%', ''))
                # Piktogramma gistogrammasi
                bar = "🟦" * (val // 10) + "⬜️" * (10 - (val // 10))
                stat_text += f"<code>{day}</code> {bar} <b>{val}%</b>\n"
            except: continue
            
    stat_text += f"\n🔥 Umumiy ball: <code>{user.get('total_score', 0)}</code>"
    bot.send_message(message.chat.id, stat_text, parse_mode='HTML')

# --- FINISH ---
@bot.message_handler(func=lambda m: m.text == "Finish 🏁")
def finish_day(message):
    uid = str(message.chat.id)
    user = get_user(uid)
    today = datetime.now().strftime('%d/%m')
    
    if any(today in entry for entry in user.get('history', [])):
        bot.send_message(uid, "Bugun yakunlab bo'lingan! ✨")
        return
    
    completed = len(user.get('completed_today', []))
    percent = int((completed / TOTAL_TASKS) * 100)
    user.setdefault('history', []).append(f"{today}: {percent}%")
    user['completed_today'] = []
    save_data()
    
    msg = f"🏁 <b>Bugungi natija: {percent}%</b>\n🔥 Umumiy ball: {user['total_score']}"
    if percent >= 30:
        try:
            bot.send_animation(uid, random.choice(GIFS), caption=f"{msg}\n\n{random.choice(FINISH_MOTIVATIONS)}", parse_mode='HTML')
        except:
            bot.send_message(uid, msg, parse_mode='HTML')
    else:
        bot.send_message(uid, f"{msg}\n\nErtaga kuchliroq bo'lamiz! 💪", parse_mode='HTML')

# --- WEBAPP MA'LUMOTI (Har bir vazifa uchun) ---
@bot.message_handler(content_types=['web_app_data'])
def web_app_receive(message):
    data = json.loads(message.web_app_data.data)
    user = get_user(message.chat.id)
    if data.get('action') == "done":
        task = data.get('task')
        if task not in user.get('completed_today', []):
            user.setdefault('completed_today', []).append(task)
            user['total_score'] = user.get('total_score', 0) + 10
            save_data()
            
            # Har bir vazifa uchun foiz hisoblash
            current_percent = int((len(user['completed_today']) / TOTAL_TASKS) * 100)
            caption = f"✅ <b>{task}</b> bajarildi!\n💰 +10 ball (Jami: {user['total_score']})\n📈 Bugungi progress: {current_percent}%\n\n{random.choice(CUSTOM_MOTIVATIONS)}"
            
            try:
                bot.send_animation(message.chat.id, random.choice(GIFS), caption=caption, parse_mode='HTML')
            except:
                bot.send_message(message.chat.id, caption, parse_mode='HTML')

# --- ADMIN PANEL ---
@bot.message_handler(commands=['admin'])
@bot.message_handler(func=lambda m: m.text == "/admin 👨‍💻")
def admin_panel(message):
    if message.chat.id == ADMIN_ID:
        bot.send_message(message.chat.id, f"👥 Jami foydalanuvchilar: {len(user_data)}\n\n/users\n/db_download")

if __name__ == "__main__":
    bot.infinity_polling()
