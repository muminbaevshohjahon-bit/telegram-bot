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

# --- ADMIN & CHANNEL ---
ADMIN_ID = 6338204692
CHANNEL_ID = "@caffeinefan"

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
TOTAL_TASKS = 8

CUSTOM_MOTIVATIONS = [
    "Sen boshlamasang, hech narsa boshlanmaydi. 🔥",
    "Bugungi og‘riq — ertangi kuch. 💪",
    "Eng zo‘r vaqt — hozir. 🚀",
    "Intizom — bu o'ziga berilgan va'dani bajarishdir. ✨",
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
    "O‘zgarish sendan boshlanadi.", "Boshlagin. Hozir. Shu yerda.", "Barakallo zo'r ketayabsan."
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
    "https://media.giphy.com/media/g9582DNuQppxC/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNGU3NGt0eTJuNHd0OXM5eXNwbWVhaDI4ODBja3pwZnhnNzZ6c3ZnYiZlcD12MV9naWZzX3RyZW5kaW5nJmN0PWc/GpyS1lJXJYupG/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3NjJ6N2Zlamg2bmRzZzduYWptcnNuc2hyNmUybG1sb21oM3gxZnp0aSZlcD12MV9naWZzX3RyZW5kaW5nJmN0PWc/h0MTqLyvgG0Ss/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZjI3Y3J0M2lva2FzYjJ0d3F2MWFtNnQ5eWFpM2I3aHM4bGNicjE4ZSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/FRzg3omGn8C5ZYeafu/giphy.gif."
]

# --- HELPER FUNCTIONS ---
def get_user(uid):
    uid = str(uid)
    if uid not in user_data:
        user_data[uid] = {'total_score': 0, 'history': [], 'completed_today': [], 'info': {}, 'step': 'start', 'current_day': 1}
    return user_data[uid]

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    web_url = f"https://muminbaevshohjahon-bit.github.io/telegram-bot/?v={random.randint(1, 999999)}"
    markup.add(KeyboardButton("Chellenjlar 🗓", web_app=WebAppInfo(url=web_url)))
    markup.add(KeyboardButton("Peshqadamlar 🏆"), KeyboardButton("Mening natijam 📊"))
    markup.add(KeyboardButton("Finish 🏁"))
    return markup

def check_subscription(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['creator', 'administrator', 'member']
    except:
        return False

def subscription_required(func):
    def wrapper(message):
        uid = message.chat.id
        if not check_subscription(uid):
            bot.send_message(uid, f"❌ Avval kanalga obuna bo‘ling: {CHANNEL_ID}")
            return
        return func(message)
    return wrapper

# --- START VA REGISTRATSIYA ---
@bot.message_handler(commands=['start'])
def start(message):
    uid = message.chat.id
    user = get_user(uid)
    if not check_subscription(uid):
        bot.send_message(uid, f"⚠️ Iltimos, kanalga obuna bo‘ling: {CHANNEL_ID}\n\nObuna bo‘lganingizdan so‘ng bot avtomatik xabar yuboradi.")
        user['step'] = 'waiting_subscription'
        save_data()
        return
    if user['step'] == 'main':
        bot.send_message(uid, "Siz allaqachon ro'yxatdan o'tgansiz!", reply_markup=main_menu())
        return
    
    # MUAMMO SHU YERDA EDI: 
    user['step'] = 'get_name'
    save_data()
    
      welcome_text = (
        "<b><i>Assalomu aleykum, hush kelibsiz!</i></b>\n"
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
    bot.send_message(message.chat.id, "Tahallus tanlang:")

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_nick')
def get_nick(message):
    uid = str(message.chat.id)
    user_data[uid]['info']['nickname'] = message.text
    user_data[uid]['step'] = 'main'
    save_data()
    bot.send_message(message.chat.id, "Tabrikleyshn, ro'yxatdan o'tdingiz!🔥", reply_markup=main_menu())


# --- ASOSIY FUNKSIYALAR ---
@bot.message_handler(func=lambda m: m.text == "Peshqadamlar 🏆")
@subscription_required
def leaderboard(message):
    users = []
    for uid, data in user_data.items():
        score = data.get('total_score', 0)
        nick = data.get('info', {}).get('nickname', "Foydalanuvchi")
        users.append({'score': score, 'nick': nick})
    users.sort(key=lambda x: x['score'], reverse=True)
    text = "🏆 <b>Eng kuchli ishtirokchilar:</b>\n\n"
    for i, u in enumerate(users[:10], 1):
        text += f"{i}. {u['nick']} — {u['score']} ball\n"
    bot.send_message(message.chat.id, text, parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "Mening natijam 📊")
@subscription_required
def my_result(message):
    uid = str(message.chat.id)
    data = get_user(uid)
    completed = len(data.get('completed_today', []))
    percent = int((completed / TOTAL_TASKS) * 100)
    progress_bar = "✅" * (percent // 10) + "⬜️" * (10 - (percent // 10))
    
    res = f"📊 <b>Natijangiz:</b>\n\n👤 Ism: {data['info'].get('name')}\n⭐ Ball: {data.get('total_score')}\n📅 Kun: {data.get('current_day')}-kun\n🎯 Bugun: {percent}%\n{progress_bar}"
    bot.send_message(uid, res, parse_mode='HTML')

# --- FINISH (YANGI MANTIQ BILAN) ---
@bot.message_handler(func=lambda m: m.text == "Finish 🏁")
@subscription_required
def finish_day(message):
    uid = str(message.chat.id)
    user = get_user(uid)
    today = datetime.now().strftime('%d/%m')
    
    if any(today in entry for entry in user.get('history', [])):
        bot.send_message(uid, "Bugun yakunlab bo'lingan! ✨")
        return

    percent = int((len(user.get('completed_today', [])) / TOTAL_TASKS) * 100)
    
    # Natija bo'yicha mantiq
    if percent < 50:
        feedback = "Yomon emas, lekin bundan ko'pini qila olasan! 💪"
    elif 50 <= percent < 90:
        feedback = "Zo'r natija! Sen bundanda ko'prog'iga loyiqsan! 🔥"
    else:
        feedback = "Malades, bo'lishi mumkin emas! 🚀"

    user.setdefault('history', []).append(f"{today}: {percent}%")
    user['completed_today'] = []
    user['current_day'] = user.get('current_day', 1) + 1
    save_data()
    
    bot.send_animation(uid, random.choice(GIFS), caption=f"🏁 Natija: {percent}%\n\n{feedback}")

# --- SCHEDULER (YANGI VAQTLAR) ---
def auto_scheduler():
    threading.Thread(target=check_subscription_periodically, daemon=True).start()
    while True:
        now = datetime.now().strftime("%H:%M")
        
        # Siz so'ragan eslatma vaqtlari
        reminders = {
            "06:00": "☀️ Xayrli tong! Yangi kun boshlandi. Chellenjlarni boshlaymizmi?",
            "09:00": "💻 Fokus vaqti! Vazifalarni bajarishni unutmang.",
            "12:00": "🥗 Kun yarmi keldi. Progressingiz qanday?",
            "15:00": "⚡️ Energiya kerakmi? Jismoniy mashqni bajaramiz!",
            "17:00": "📚 Kitob mutolaasi uchun ayni vaqt.",
            "19:00": "🌙 Kechki payt bo'shashmang, ozgina qoldi!",
            "22:00": "🔔 Kun yakunlanmoqda! Finish 🏁 tugmasini bosishni unutmang!"
        }

        if now in reminders:
            for uid in list(user_data.keys()):
                try: bot.send_message(uid, reminders[now])
                except: pass
            time.sleep(61)
        
        # Avtomatik tunda yopish (23:59)
        if now == "23:59":
            today = datetime.now().strftime('%d/%m')
            for uid, data in user_data.items():
                if not any(today in entry for entry in data.get('history', [])):
                    p = int((len(data.get('completed_today', [])) / TOTAL_TASKS) * 100)
                    data.setdefault('history', []).append(f"{today}: {p}%")
                    data['completed_today'] = []
                    data['current_day'] = data.get('current_day', 1) + 1
            save_data()
            time.sleep(61)
        time.sleep(30)

# --- WEBAPP VA OBUNA ---
@bot.message_handler(content_types=['web_app_data'])
def web_app_receive(message):
    data = json.loads(message.web_app_data.data)
    user = get_user(message.chat.id)
    if data.get('action') == "done":
        task = data.get('task')
        if task not in user.get('completed_today', []):
            user.setdefault('completed_today', []).append(task)
            user['total_score'] += 10
            save_data()
            bot.send_message(message.chat.id, f"✅ {task} bajarildi! +10 ball\n\n{random.choice(CUSTOM_MOTIVATIONS)}")

def check_subscription_periodically():
    while True:
        for uid in list(user_data.keys()):
            user = user_data[uid]
            if user.get('step') == 'waiting_subscription' and check_subscription(uid):
                user['step'] = 'get_name'
                save_data()
                bot.send_message(uid, "🎉 Obuna tasdiqlandi! Ismingizni kiriting:")
        time.sleep(10)

if __name__ == "__main__":
    threading.Thread(target=auto_scheduler, daemon=True).start()
    bot.infinity_polling()
