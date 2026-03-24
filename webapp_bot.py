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

ADMIN_ID = 6338204692 
CHANNELS = ["@mbe_useful"] 
TOTAL_TASKS = 8 

# --- DATA ---
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
    "https://media.giphy.com/media/8ZblO3ZD5NMltPaFS2/giphy.gif",
    "https://media.giphy.com/media/g9582DNuQppxC/giphy.gif"
]



# --- HELPERS ---
def check_sub(uid):
    for channel in CHANNELS:
        try:
            status = bot.get_chat_member(channel, uid).status
            if status in ['left', 'kicked']:
                return False
        except Exception as e:
            print("SUB ERROR:", e)
            return False
    return True

def get_user(uid):
    uid = str(uid)
    if uid not in user_data:
        user_data[uid] = {
            'total_score': 0,
            'history': [],
            'completed_today': [],
            'info': {},
            'step': 'start'
        }
    return user_data[uid]

def main_menu(uid):
    uid = str(uid)
    user = get_user(uid)

    current_day = len(user.get('history', [])) + 1
    if current_day > 30:
        current_day = 30

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    web_url = f"https://muminbaevshohjahon-bit.github.io/telegram-bot/?day={current_day}&v={random.randint(1,999999)}"

    markup.add(KeyboardButton("Chellenjlar🗓", web_app=WebAppInfo(url=web_url)))
    markup.add(KeyboardButton("Peshqadamlar 🏆"), KeyboardButton("Mening natijam 📊"))
    markup.add(KeyboardButton("Finish 🏁"))

    if int(uid) == ADMIN_ID:
        markup.add(KeyboardButton("/admin 👨‍💻"))

    return markup

# --- WEB APP DATA (FIX QILINGAN) ---
@bot.message_handler(content_types=['web_app_data'])
def web_app_receive(message):
    uid = str(message.chat.id)
    user = get_user(uid)

    try:
        data = json.loads(message.web_app_data.data)  # ✅ JSON parse
        task_id = data.get("task")
        day = data.get("day")
    except:
        return

    key = f"{task_id}_{day}"  # ✅ unique key

    if key not in user.get('completed_today', []):
        user.setdefault('completed_today', []).append(key)
        user['total_score'] = user.get('total_score', 0) + 10

        save_data()

        # ✅ GIF + motivatsiya qo‘shildi
        gif = random.choice(GIFS)
        motivation = random.choice(FINISH_MOTIVATIONS)

        bot.send_animation(
            uid,
            gif,
            caption=f"{motivation}\n\n+10 ball 🔥"
        )

# --- REMINDER (o‘zgartirmadim faqat xavfsiz qildim) ---
def reminder_thread():
    while True:
        now = datetime.now().strftime("%H:%M")
        if now in ["08:00", "12:00", "18:00", "21:00"]:
            msg = random.choice(CUSTOM_MOTIVATIONS)
            for uid in list(user_data.keys()):
                try:
                    bot.send_message(uid, f"🔔 {msg}")
                except:
                    continue
            time.sleep(61)
        time.sleep(30)

threading.Thread(target=reminder_thread, daemon=True).start()

# --- START VA REGISTRATSIYA ---
@bot.message_handler(commands=['start'])
def start(message):
    uid = str(message.chat.id)
    user_data[uid] = {'total_score': 0, 'history': [], 'completed_today': [], 'info': {}, 'step': 'get_name'}
    save_data()
    welcome_text = (
        "<b><i>Assalomu aleykum hush kelibsiz!</i></b>\n"
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
    bot.send_message(message.chat.id, "Tug‘ilgan yilingiz (masalan: 2004):")

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_year')
def get_year(message):
    uid = str(message.chat.id)
    user_data[uid]['info']['birth_year'] = message.text
    user_data[uid]['step'] = 'get_month'
    save_data()
    bot.send_message(message.chat.id, "Tug‘ilgan oyingiz (masalan: Avgust):")

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_month')
def get_month(message):
    uid = str(message.chat.id)
    user_data[uid]['info']['birth_month'] = message.text
    user_data[uid]['step'] = 'get_day'
    save_data()
    bot.send_message(message.chat.id, "Tug‘ilgan kuningiz (masalan: 25):")

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_day')
def get_day(message):
    uid = str(message.chat.id)
    user_data[uid]['info']['birth_day'] = message.text
    user_data[uid]['step'] = 'get_nick'
    save_data()
    bot.send_message(message.chat.id, "Nickname kiriting:")

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_nick')
def get_nick(message):
    uid = str(message.chat.id)
    user_data[uid]['info']['nickname'] = message.text
    user_data[uid]['step'] = 'main'
    save_data()
    bot.send_message(message.chat.id, "Tabrikleyshn, Ro'yxatdan o'tildi!🔥", reply_markup=main_menu())


# --- LEADERBOARD ---
@bot.message_handler(func=lambda m: m.text == "Peshqadamlar 🏆")
def leaderboard(message):
    if not check_sub(message.chat.id):
        return

    sorted_users = sorted(user_data.items(), key=lambda x: x[1].get('total_score', 0), reverse=True)

    text = "🏆 TOP:\n\n"
    for i, (uid, data) in enumerate(sorted_users[:10], 1):
        name = data.get('info', {}).get('name', "User")
        score = data.get('total_score', 0)
        text += f"{i}. {name} — {score}\n"

    bot.send_message(message.chat.id, text)

# --- STATS ---
@bot.message_handler(func=lambda m: m.text == "Mening natijam 📊")
def stats(message):
    if not check_sub(message.chat.id):
        return

    user = get_user(message.chat.id)

    percent = int((len(set(user.get('completed_today', []))) / TOTAL_TASKS) * 100)

    bot.send_message(message.chat.id, f"Bugungi natija: {percent}%")

# --- FINISH ---
@bot.message_handler(func=lambda m: m.text == "Finish 🏁")
def finish(message):
    if not check_sub(message.chat.id):
        return

    uid = str(message.chat.id)
    user = get_user(uid)

    today = datetime.now().strftime('%d/%m')

    if any(today in h for h in user.get('history', [])):
        bot.send_message(uid, "Bugun allaqachon yopilgan!")
        return

    percent = int((len(set(user.get('completed_today', []))) / TOTAL_TASKS) * 100)

    user.setdefault('history', []).append(f"{today}: {percent}%")
    user['completed_today'] = []

    save_data()

    bot.send_message(uid, f"Kun yopildi: {percent}%", reply_markup=main_menu(uid))

# --- RUN ---
bot.infinity_polling()
