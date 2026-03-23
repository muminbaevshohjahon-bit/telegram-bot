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
    "O‘zgarish sendan boshlanadi.", "Boshlagin. Hozir. Shu yerda.","Aqilli inson uchun har kuni yangi kun boshlanadi.","Kuchsizlar faqat taslim bo'ladi."
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

def get_user(uid):
    uid = str(uid)
    if uid not in user_data:
        user_data[uid] = {'total_score': 0, 'history': [], 'completed_today': [], 'info': {}, 'step': 'start'}
    return user_data[uid]

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    # ?v={random} kalendarni nollashtirishga yordam beradi
    web_url = f"https://muminbaevshohjahon-bit.github.io/telegram-bot/?v={random.randint(1, 999999)}"
    markup.add(KeyboardButton("Chellenjlar 🗓", web_app=WebAppInfo(url=web_url)))
    markup.add(KeyboardButton("Peshqadamlar 🏆"), KeyboardButton("Mening natijam 📊"))
    markup.add(KeyboardButton("Finish 🏁"))
    return markup

# --- START VA REGISTRATSIYA (NOLLASHTIRISH SHU YERDA) ---
@bot.message_handler(commands=['start'])
def start(message):
    uid = str(message.chat.id)
    # Foydalanuvchi start bossa, hamma narsasi nollanadi
    user_data[uid] = {'total_score': 0, 'history': [], 'completed_today': [], 'info': {}, 'step': 'get_name'}
    save_data()
    welcome_text = (
        "<b><i>Assalomu aleykum hush kelibsiz!</i></b>\n"
        "<b><i>Men MBE useful tomonidan yaratilgan botman!</i></b>\n\n"
        "<b><i>Maqsadimiz 30 kunlik chellenj davomida intizomni shakllantirish.</i></b>\n\n"
        "Keling tanishib olaylik... Ismingizni kiriting:"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode='HTML')

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_name')
def get_name(message):
    uid = str(message.chat.id); user_data[uid]['info']['name'] = message.text
    user_data[uid]['step'] = 'get_year'; save_data()
    bot.send_message(message.chat.id, "Tug‘ilgan yilingiz (masalan: 2004):")

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_year')
def get_year(message):
    uid = str(message.chat.id); user_data[uid]['info']['birth_year'] = message.text
    user_data[uid]['step'] = 'get_month'; save_data()
    bot.send_message(message.chat.id, "Tug‘ilgan oyingiz (masalan: Avgust):")

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_month')
def get_month(message):
    uid = str(message.chat.id); user_data[uid]['info']['birth_month'] = message.text
    user_data[uid]['step'] = 'get_day'; save_data()
    bot.send_message(message.chat.id, "Tug‘ilgan kuningiz (masalan: 25):")

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_day')
def get_day(message):
    uid = str(message.chat.id); user_data[uid]['info']['birth_day'] = message.text
    user_data[uid]['step'] = 'get_nick'; save_data()
    bot.send_message(message.chat.id, "Nickname kiriting:")

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_nick')
def get_nick(message):
    uid = str(message.chat.id); user_data[uid]['info']['nickname'] = message.text
    user_data[uid]['step'] = 'main'; save_data()
    bot.send_message(message.chat.id, "Tabrikleyshn, Ro'yxatdan o'tildi!🔥", reply_markup=main_menu())

# --- ADMIN PANEL FUNKSIYALARI ---
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.chat.id == ADMIN_ID:
        total = len(user_data)
        text = f"👨‍💻 <b>Admin Panel</b>\n\n👥 Jami foydalanuvchilar: {total}\n\n/users - Ro'yxat\n/db_download - Bazani yuklab olish"
        bot.send_message(message.chat.id, text, parse_mode='HTML')

@bot.message_handler(commands=['users'])
def list_users(message):
    if message.chat.id == ADMIN_ID:
        text = "📋 <b>Foydalanuvchilar:</b>\n\n"
        for uid, data in user_data.items():
            name = data.get('info', {}).get('name', "Noma'lum")
            nick = data.get('info', {}).get('nickname', "Yo'q")
            score = data.get('total_score', 0)
            text += f"👤 {name} (@{nick}) — {score} ball\n"
        bot.send_message(message.chat.id, text, parse_mode='HTML')

@bot.message_handler(commands=['db_download'])
def send_db(message):
    if message.chat.id == ADMIN_ID:
        with open('users_db.json', 'rb') as f:
            bot.send_document(message.chat.id, f)
# --- PESHQADAMLAR (ISHMAYOTGAN QISM TO'G'RILANDI) ---
@bot.message_handler(func=lambda m: m.text == "Peshqadamlar 🏆")
def leaderboard(message):
    users = []
    for uid, data in user_data.items():
        if 'info' in data and 'nickname' in data['info']:
            users.append({'nick': data['info']['nickname'], 'score': data.get('total_score', 0)})
    
    if not users:
        bot.send_message(message.chat.id, "Hali hech kim ro'yxatdan o'tmagan.")
        return

    users.sort(key=lambda x: x['score'], reverse=True)
    text = "🏆 <b>Eng kuchli ishtirokchilar:</b>\n\n"
    for i, u in enumerate(users[:10], 1):
        text += f"{i}. {u['nick']} — {u['score']} ball\n"
    
    bot.send_message(message.chat.id, text, parse_mode='HTML')

# --- MENING NATIJAM ---
@bot.message_handler(func=lambda m: m.text == "Mening natijam 📊")
def my_stats(message):
    user = get_user(message.chat.id)
    history = user.get('history', [])
    stat_text = "📊 <b>Natijalar:</b>\n\n"
    if not history: stat_text += "Hali natija yo'q."
    else:
        for entry in history[-7:]:
            try:
                day, res = entry.split(": ")
                icon = "✅" if "100%" in res else "📈"
                stat_text += f"{icon} {day}: {res}\n"
            except: continue
    stat_text += f"\n🔥 Umumiy ball: {user.get('total_score', 0)}"
    bot.send_message(message.chat.id, stat_text, parse_mode='HTML')

# --- FINISH (50% DAN PAST BO'LSA GIF JO'NATILMAYDI) ---
@bot.message_handler(func=lambda m: m.text == "Finish 🏁")
def finish_day(message):
    user = get_user(message.chat.id)
    today = datetime.now().strftime('%d/%m')
    if any(today in entry for entry in user.get('history', [])):
        bot.send_message(message.chat.id, "Bugun yakunlab bo'lingan! ✨")
        return
    
    percent = int((len(user.get('completed_today', [])) / TOTAL_TASKS) * 100)
    user.setdefault('history', []).append(f"{today}: {percent}%")
    user['completed_today'] = []; save_data()
    
    if percent >= 50:
        motivation = random.choice(FINISH_MOTIVATIONS)
        bot.send_animation(message.chat.id, random.choice(GIFS), caption=f"🏁 Natija: {percent}%\n\n{motivation}", parse_mode='HTML')
    else:
        # 50% dan past bo'lsa faqat matn
        bot.send_message(message.chat.id, f"🏁 Natija: {percent}%\n\nErtaga kuchliroq bo'lamiz! 💪", parse_mode='HTML')

# --- SCHEDULER (NOTIFICATIONS & AUTO-FINISH) ---
def auto_scheduler():
    while True:
        now = datetime.now().strftime("%H:%M")
        if now == "08:00":
            for uid in user_data.keys():
                try: bot.send_message(uid, "☀️ Xayrli tong! Bugun 7 ta vazifani ham yoramizmi?")
                except: pass
            time.sleep(61)
        if now == "21:00":
            for uid in user_data.keys():
                try: bot.send_message(uid, "🔔 Kun yakunlanmoqda, Finish tugmasini bosishni unutmang!")
                except: pass
            time.sleep(61)
        if now == "23:00":
            today = datetime.now().strftime('%d/%m')
            for uid, data in user_data.items():
                if not any(today in entry for entry in data.get('history', [])):
                    completed = len(data.get('completed_today', []))
                    percent = int((completed / TOTAL_TASKS) * 100)
                    data.setdefault('history', []).append(f"{today}: {percent}%")
                    data['completed_today'] = []
            save_data()
            time.sleep(61)
        time.sleep(30)

threading.Thread(target=auto_scheduler, daemon=True).start()

# --- WEBAPP DATA ---
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
    bot.infinity_polling()
