import telebot
import os
import random
import json
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
        with open('{}', 'r') as f:
            return json.load(f)
    except:
        return {}
        
def save_data():
    with open('{}', 'w') as f:
        json.dump(user_data, f)

user_data = load_data()
TOTAL_TASKS = 7

# SIZ ISTAGAN TO'LIQ MOTIVATSIYALAR RO'YXATI
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
    web_url = "https://muminbaevshohjahon-bit.github.io/telegram-bot/" 
    markup.add(KeyboardButton("Chellenjlar 🗓", web_app=WebAppInfo(url=web_url)))
    markup.add(KeyboardButton("Peshqadamlar 🏆"), KeyboardButton("Mening natijam 📊"))
    markup.add(KeyboardButton("Finish 🏁"))
    return markup

# --- LOGIKA ---
@bot.message_handler(commands=['start'])
def start(message):
    uid = str(message.chat.id)
    
    # MUHIM: Xotirani va WebApp katakchalarini to'liq nollash
    user_data[uid] = {
        'total_score': 0, 
        'history': [], 
        'completed_today': [], 
        'info': {}, 
        'step': 'get_name'
    }
    save_data() # Faylga yozish
    
    welcome_text = (
        "<b><i>Assalomu aleykum hush kelibsiz!</i></b>\n"
        "<b><i>Men MBE useful tomonidan yaratilgan botman!</i></b>\n\n"
        "<b><i>Maqsadimiz 30 kunlik chellenj davomida intizomni shakllantirish.</i></b>\n"
        "<b><i>Balki foydasi tegar...</i></b>\n\n"
        "Keling tanishib olaylik... Ismingizni kiriting:"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode='HTML')

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_name')
def get_name(message):
    user = get_user(message.chat.id)
    user['info']['name'] = message.text
    user['step'] = 'get_birth'
    save_data()
    bot.send_message(message.chat.id, "Tug‘ilgan yilingiz (masalan, 2004):")

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_birth')
def get_birth(message):
    user = get_user(message.chat.id)
    user['info']['birth_year'] = message.text
    user['step'] = 'get_month'
    save_data()
    bot.send_message(message.chat.id, "Tug‘ilgan oyingiz:")

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_month')
def get_month(message):
    user = get_user(message.chat.id)
    user['info']['birth_month'] = message.text
    user['step'] = 'get_day'
    save_data()
    bot.send_message(message.chat.id, "Tug‘ilgan kuningiz:")

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_day')
def get_day(message):
    user = get_user(message.chat.id)
    user['info']['birth_day'] = message.text
    user['step'] = 'get_nick'
    save_data()
    bot.send_message(message.chat.id, "Reyting uchun <b>Nickname</b> kiriting:", parse_mode='HTML')

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_nick')
def get_nick(message):
    user = get_user(message.chat.id)
    user['info']['nickname'] = message.text
    user['step'] = 'main'
    pid = f"MBE-{random.randint(10000, 99999)}"
    user['info']['public_id'] = pid
    save_data()
    bot.send_message(message.chat.id, f"Tabrikleyshn, muvaffaqiyatli ro'yxatdan o'tdingiz!🔥\nSizning ID: <b>{pid}</b>", parse_mode='HTML', reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == "Finish 🏁")
def finish_day(message):
    user = get_user(message.chat.id)
    today = datetime.now().strftime('%d/%m')
    
    # Bugun allaqachon tugatgan bo'lsa eslatma
    if any(today in entry for entry in user['history']):
        bot.send_message(message.chat.id, "Bugun uchun vazifalar yakunlangan. Ertaga ko'rishguncha! ✨")
        return

    completed_tasks = user.get('completed_today', [])
    percent = int((len(completed_tasks) / TOTAL_TASKS) * 100)
    
    user['history'].append(f"{today}: {percent}%")
    user['completed_today'] = [] 
    save_data()

    motivation = random.choice(FINISH_MOTIVATIONS)
    msg = f"🏁 <b>Natija: {percent}%</b>\n\n{motivation}"

    try:
        bot.send_animation(message.chat.id, random.choice(GIFS), caption=msg, parse_mode='HTML')
    except:
        bot.send_message(message.chat.id, msg, parse_mode='HTML')

@bot.message_handler(content_types=['web_app_data'])
def web_app_receive(message):
    data = json.loads(message.web_app_data.data)
    user = get_user(message.chat.id)
    if data.get('action') == "done":
        task = data.get('task')
        if task not in user.get('completed_today', []):
            user['completed_today'].append(task)
            user['total_score'] += 10
            save_data()
            bot.send_message(message.chat.id, f"✅ {task} bajarildi!\n{random.choice(CUSTOM_MOTIVATIONS)}")

# Peshqadamlar va Mening natijam funksiyalari o'z holicha qoladi...

if __name__ == "__main__":
    bot.infinity_polling()
