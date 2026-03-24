import telebot
import os
import random
import json
import threading
import time
from datetime import datetime
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

# Vaqt zonasi - O'zbekiston vaqti bilan ishlash uchun
os.environ['TZ'] = 'Asia/Tashkent'
if hasattr(time, 'tzset'):
    time.tzset()

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# --- KONFIGURATSIYA ---
ADMIN_ID = 6338204692 
CHANNELS = ["@mbe_useful"] # Majburiy obuna kanali
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
    for channel in CHANNELS:
        try:
            status = bot.get_chat_member(channel, uid).status
            if status == 'left': return False
        except: continue
    return True

def get_user(uid):
    uid = str(uid)
    if uid not in user_data:
        user_data[uid] = {'total_score': 0, 'history': [], 'completed_today': [], 'info': {}, 'step': 'start'}
    return user_data[uid]

def main_menu(uid):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    # WebApp URL keshni tozalash uchun random son bilan
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

    user_data[str(uid)] = {'total_score': 0, 'history': [], 'completed_today': [], 'info': {}, 'step': 'get_name'}
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

# --- NATIJALAR ---
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

# --- KUNNI YAKUNLASH ---
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
    
    if percent >= 20:
        motivation = random.choice(FINISH_MOTIVATIONS)
        bot.send_animation(uid, random.choice(GIFS), caption=f"🏁 Natija: {percent}%\n\n{motivation}", parse_mode='HTML')
    else:
        bot.send_message(uid, f"🏁 Natija: {percent}%\n\nBugun biroz sustkashlik bo'ldi. Ertaga kuchliroq bo'lamiz! 💪")

# --- WEBAPP MA'LUMOTLARI ---
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
            p = int((len(user['completed_today']) / TOTAL_TASKS) * 100)
            bot.send_message(message.chat.id, f"✅ <b>{task}</b> bajarildi!\n📈 Progress: {p}%\n\n{random.choice(CUSTOM_MOTIVATIONS)}", parse_mode='HTML')

# --- AVTOMATIK ESLATMALAR ---
def auto_scheduler():
    while True:
        now = datetime.now().strftime("%H:%M")
        
        # Vaqtlar ro'yxati
        schedules = {
            "08:00": "☀️ Xayrli tong! Bugun 8 ta vazifani (uyqu bilan) ham yoramizmi?",
            "12:00": "🕛 Kun yarmi keldi! Vazifalar qanday ketyapti? Orqada qolib ketmang! 💪",
            "19:00": "🌆 Kech kirib qoldi. Bugun hamma vazifalarni bajarishga ulguramizmi? Harakatni tezlashtiramiz! 🚀",
            "23:00": "🌙 Soat 23:00. Uyqu vaqti bo'ldi! Finish tugmasini bosing va dam oling."
        }

        if now in schedules:
            for uid in list(user_data.keys()):
                try: 
                    bot.send_message(uid, schedules[now])
                except: pass
            time.sleep(61) # Bir xil xabar qayta ketmasligi uchun

        time.sleep(30)

threading.Thread(target=auto_scheduler, daemon=True).start()

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
            bot.send_message(message.chat.id, "Baza fayli topilmadi.")

if __name__ == "__main__":
    bot.infinity_polling()
