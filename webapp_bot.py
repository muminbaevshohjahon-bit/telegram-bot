import telebot
import os
import random
import json
import threading
import time
from datetime import datetime
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

# Vaqt zonasi
os.environ['TZ'] = 'Asia/Tashkent'
if hasattr(time, 'tzset'):
    time.tzset()

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

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
TOTAL_TASKS = 7

# SIZNING BARCHA MOTIVATSIYALARINGIZ
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
    "O‘zgarish sendan boshlanadi.", "Boshlagin. Hozir. Shu yerda."
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
    "https://media.giphy.com/media/3o7TKDkDbIDJieKbVm/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaXU3bGl0dXg3c3FxM3VuZnl1ZW8wamRlbW5vbncxN2V1enNoNjhxOCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/8ZblO3ZD5NMltPaFS2/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaXU3bGl0dXg3c3FxM3VuZnl1ZW8wamRlbW5vbncxN2V1enNoNjhxOCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/g9582DNuQppxC/giphy.gif",
    "https://media.giphy.com/media/FACfMgP1N9mlG/giphy.gif"
]

def get_user(uid):
    uid = str(uid)
    if uid not in user_data:
        user_data[uid] = {'total_score': 0, 'history': [], 'completed_today': [], 'info': {}, 'step': 'start'}
    return user_data[uid]

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    # Keshni tozalash uchun tasodifiy son qo'shilgan URL
    web_url = f"https://muminbaevshohjahon-bit.github.io/telegram-bot/?v={random.randint(1, 999)}"
    markup.add(KeyboardButton("Chellenjlar 🗓", web_app=WebAppInfo(url=web_url)))
    markup.add(KeyboardButton("Peshqadamlar 🏆"), KeyboardButton("Mening natijam 📊"))
    markup.add(KeyboardButton("Finish 🏁"))
    return markup

# --- AVTOMATIK FUNKSIYALAR (ESLATMA VA FINISH) ---
def auto_scheduler():
    while True:
        now = datetime.now().strftime("%H:%M")
        
        # 1. Avtomat Finish (23:00 da)
        if now == "23:00":
            today = datetime.now().strftime('%d/%m')
            for uid, data in user_data.items():
                if not any(today in entry for entry in data.get('history', [])):
                    completed = len(data.get('completed_today', []))
                    percent = int((completed / TOTAL_TASKS) * 100)
                    data.setdefault('history', []).append(f"{today}: {percent}%")
                    data['completed_today'] = []
                    try:
                        bot.send_message(uid, f"🌙 <b>Kun yakunlandi!</b>\nBugungi natijangiz: <b>{percent}%</b>", parse_mode='HTML')
                    except: pass
            save_data()
            time.sleep(61)

        # 2. Ertalabki eslatma (08:00 da)
        if now == "08:00":
            for uid in user_data.keys():
                try:
                    bot.send_message(uid, "☀️ <b>Xayrli tong!</b>\nBugun yangi kun, yangi imkoniyatlar. Chellenjlarni boshlaymizmi?", parse_mode='HTML')
                except: pass
            time.sleep(61)

        time.sleep(30)

threading.Thread(target=auto_scheduler, daemon=True).start()

# --- BOT LOGIKASI ---
@bot.message_handler(commands=['start'])
def start(message):
    uid = str(message.chat.id)
    
    # ID-ni butunlay nollash
    user_data[uid] = {
        'total_score': 0, 
        'history': [], 
        'completed_today': [], 
        'info': {}, 
        'step': 'get_name'
    }
    save_data()
    
  welcome_text = (
        "<b><i>Assalomu aleykum hush kelibsiz!</i></b>\n"
        "<b><i>Men MBE useful tomonidan yaratilgan botman!</i></b>\n\n"
        "<b><i>Maqsadimiz 30 kunlik chellenj davomida intizomni shakllantirish.</i></b>\n"
        "<b><i>Balki foydasi tegar...</i></b>\n\n"
        "Keling tanishib olaylik... Ismingizni kiriting:"
    )
    
    bot.send_message(message.chat.id, welcome_text, parse_mode='HTML')

# Ro'yxatdan o'tish qismlari (get_name, get_birth, va h.k.) o'z holicha qoladi...
# [Sizdagi mavjud ro'yxatdan o'tish funksiyalarini shu yerga qo'shib qo'ying]

@bot.message_handler(func=lambda m: m.text == "Finish 🏁")
def finish_day(message):
    user = get_user(message.chat.id)
    today = datetime.now().strftime('%d/%m')
    
    if any(today in entry for entry in user.get('history', [])):
        bot.send_message(message.chat.id, "Bugun yakunlab bo'lingan! ✨")
        return

    completed_count = len(user.get('completed_today', []))
    percent = int((completed_count / TOTAL_TASKS) * 100)
    
    user.setdefault('history', []).append(f"{today}: {percent}%")
    user['completed_today'] = [] 
    save_data()

    motivation = random.choice(FINISH_MOTIVATIONS)
    msg = f"🏁 <b>Natija: {percent}%</b>\n\n{motivation}"
    bot.send_message(message.chat.id, msg, parse_mode='HTML')

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
            bot.send_message(message.chat.id, f"✅ {task} bajarildi!\n{random.choice(CUSTOM_MOTIVATIONS)}")

if __name__ == "__main__":
    bot.infinity_polling()S
