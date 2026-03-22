import telebot
import os
import random
import json
import threading
import time
from datetime import datetime
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

# Vaqt zonasini to'g'rilash
os.environ['TZ'] = 'Asia/Tashkent'
if hasattr(time, 'tzset'):
    time.tzset()

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# --- DATA STORAGE ---
def load_data():
    if os.path.exists('users_db.json'):
        with open('users_db.json', 'r') as f:
            try: return json.load(f)
            except: return {}
    return {}

def save_data():
    with open('users_db.json', 'w') as f:
        json.dump(user_data, f)

user_data = load_data()
TOTAL_TASKS = 7

# Motivatsiyalar (Bu yerga 100 ta motivatsiyani qo'shishingiz mumkin)
CUSTOM_MOTIVATIONS = [
    "Sen boshlamasang, hech narsa boshlanmaydi. 🔥",
    "Bugungi og‘riq — ertangi kuch. 💪",
    "Eng zo‘r vaqt — hozir. 🚀"
        "Sen boshlamasang, hech narsa boshlanmaydi.", "Mukammallikni kutma — harakatni boshlash muhim.",
    "Bugungi og‘riq — ertangi kuch.", "Sen o‘ylagandan ham kuchlisan.",
    "Hech kim seni qutqarmaydi — o‘zingni o‘zing ko‘tar.", "Qiyinchilik — bu yashirin imkoniyat.",
    "Orzular faqat harakat bilan haqiqatga aylanadi.", "Qo‘rqish — o‘sish boshlanishidir.",
    "Har kuni kichik qadam — katta natija.", "Sen taslim bo‘lmaguningcha, yutqazmading.",
    "Eng katta raqibing — kechagi o‘zing.", "Bahonalar seni orqaga tortadi.",
    "Harakat — motivatsiyadan muhimroq.", "Vaqt ketmoqda — senchi?",
    "Sen bunga loyiqsan — lekin ishlashing kerak.", "Og‘ir bo‘lsa ham davom et.",
    "O‘zgarish og‘riqli, lekin zarur.", "Qanchalik qiynalsang, shunchalik kuchli bo‘lasan.",
    "Natija sabrni yaxshi ko‘radi.", "Bugun qilmaganing — ertaga pushaymon bo‘ladi.",
    "Sen o‘zingning hayoting uchun javobgarsan.", "Kichik boshlashdan uyalmagin.",
    "Har kuni o‘zingni yeng.", "Kuch — ichingda. Uni uyg‘ot.",
    "Taslim bo‘lish — eng oson yo‘l.", "Eng yaxshi vaqt — hozir.",
    "Qancha ko‘p harakat, shuncha kam pushaymon.", "Qiyinchilik seni sinaydi, sindirmaydi.",
    "Yutuq — intizom natijasi.", "Orzularing seni kutmaydi.",
    "Qo‘rquv ortida — erkinlik bor.", "Hech kim senga majbur emas — o‘zingni isbotla.",
    "Harakat qil, hatto mukammal bo‘lmasa ham.", "Yiqildingmi? Tur va davom et.",
    "Sen hali boshlamading ham.", "Qanchalik ko‘p urinma, shunchalik yaqinlashasan.",
    "Og‘riq vaqtinchalik — natija abadiy.", "Bugungi mehnat — ertangi faxr.",
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
    "Sen hech qachon yolg‘iz emassan — o‘zing bor.","Qodirali boshla", "Boshlagin. Hozir. Shu yerda."
]


FINISH_MOTIVATIONS = [
    "Dahshat! Vapshe zo'r, barakalla! 🔥",
    "Sen o'ylagandan ham kuchlisan, davom et! 💪",
    "Intizom — bu o'zingga bo'lgan hurmat. Zo'r ketyapsan! 🌟"
]

GIFS = ["https://media.giphy.com/media/FACfMgP1N9mlG/giphy.gif"]

# --- HELPERS ---
def get_user(uid):
    uid = str(uid)
    if uid not in user_data:
        user_data[uid] = {
            'total_score': 0, 'history': [], 'completed_today': [],
            'info': {}, 'step': 'start'
        }
    return user_data[uid]

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    web_url = "https://muminbaevshohjahon-bit.github.io/telegram-bot/" 
    markup.add(KeyboardButton("Kabinet 📱", web_app=WebAppInfo(url=web_url)))
    markup.add(KeyboardButton("Peshqadamlar 🏆"), KeyboardButton("Finish 🏁"))
    return markup

# --- REGISTRATION PROCESS ---
@bot.message_handler(commands=['start'])
def start(message):
    user = get_user(message.chat.id)
    text = (
        "<b>Assalomu alaykum! Xush kelibsiz!</b>\n"
        "Bu bot MBE Useful tomonidan yaratilgan 30 kunlik chellenj testi.\n\n"
        "<i>Foydasi tegsa duo qilib qo’ying.</i>\n\n"
        "Keling tanishib olamiz!\n<b>Ismingiz:</b>"
    )
    user['step'] = 'get_name'
    save_data()
    bot.send_message(message.chat.id, text, parse_mode='HTML')

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_name')
def get_name(message):
    user = get_user(message.chat.id)
    user['info']['name'] = message.text
    user['step'] = 'get_year'
    save_data()
    bot.send_message(message.chat.id, "<b>Tug‘ilgan yilingiz:</b>", parse_mode='HTML')

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_year')
def get_year(message):
    user = get_user(message.chat.id)
    user['info']['birth_year'] = message.text
    user['step'] = 'get_month'
    save_data()
    bot.send_message(message.chat.id, "<b>Tug‘ilgan oyingiz:</b>", parse_mode='HTML')

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_month')
def get_month(message):
    user = get_user(message.chat.id)
    user['info']['birth_month'] = message.text
    user['step'] = 'get_day'
    save_data()
    bot.send_message(message.chat.id, "<b>Tug‘ilgan kuningiz:</b>", parse_mode='HTML')

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_day')
def get_day(message):
    user = get_user(message.chat.id)
    user['info']['birth_day'] = message.text
    user['info']['nickname'] = user['info']['name'] # Ismini nickname sifatida saqlaymiz
    user['step'] = 'main'
    save_data()
    bot.send_message(
        message.chat.id, 
        "<b>Tabriklayman muvaffaqiyatli ro‘yxatdan o‘tdingiz!</b>\n\nQani unda boshladik! 🚀", 
        parse_mode='HTML', 
        reply_markup=main_menu()
    )

# --- BOT LOGIC ---
@bot.message_handler(content_types=['web_app_data'])
def web_app_receive(message):
    data = json.loads(message.web_app_data.data)
    user = get_user(message.chat.id)
    if data.get('action') == "done":
        task = data.get('task')
        if task not in user['completed_today']:
            user['completed_today'].append(task)
            user['total_score'] += 10
            save_data()
            bot.send_message(message.chat.id, f"✅ {task} bajarildi!\n\n{random.choice(CUSTOM_MOTIVATIONS)}")

@bot.message_handler(func=lambda m: m.text == "Peshqadamlar 🏆")
def leaderboard(message):
    sorted_u = sorted(user_data.items(), key=lambda x: x[1].get('total_score', 0), reverse=True)[:10]
    text = "🏆 <b>TOP 10 PESHQADAMLAR</b>\n\n"
    for i, (uid, data) in enumerate(sorted_u):
        name = data.get('info', {}).get('name', 'User')
        text += f"{i+1}. {name} — {data.get('total_score', 0)} ball\n"
    bot.send_message(message.chat.id, text, parse_mode='HTML')

@bot.message_handler(func=
