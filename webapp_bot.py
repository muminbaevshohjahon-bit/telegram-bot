import telebot
import os
import random
import json
import threading
import time
from datetime import datetime
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

# Vaqt zonasini to'g'rilash (Railway uchun)
os.environ['TZ'] = 'Asia/Tashkent'
time.tzset()

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# --- MA'LUMOTLAR ---
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

# SHU YERGA 100 TA MOTIVATSIYANI QO'SHING
CUSTOM_MOTIVATIONS = [
    "Sen boshlamasang, hech narsa boshlanmaydi. 🔥",
    "Bugungi og‘riq — ertangi kuch. 💪",
    "Eng zo‘r vaqt — hozir. 🚀",
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
    "Sen hech qachon yolg‘iz emassan — o‘zing bor.", "Qodirali haliyam o'tiribsanmi","Boshlagin. Hozir. Shu yerda."
]

FINISH_MOTIVATIONS = [
    "Dahshat! Vapshe zo'r, barakalla! 🔥",
    "Sen o'ylagandan ham kuchlisan, davom et! 💪",
    "Intizom — bu o'zingga bo'lgan hurmat. Zo'r ketyapsan! 🌟",
    "Bugun kechagidan yaxshiroq bo'lding. Ofarin! 👏"
]

GIFS = ["https://media.giphy.com/media/FACfMgP1N9mlG/giphy.gif"]

# --- YORDAMCHI FUNKSIYALAR ---
def get_user(uid):
    uid = str(uid)
    if uid not in user_data:
        user_data[uid] = {
            'total_score': 0, 'history': [], 'completed_today': [],
            'info': {}, 'step': 'start'
        }
    return user_data[uid]

def get_mouse_info(uid):
    sorted_users = sorted(user_data.items(), key=lambda x: x[1].get('total_score', 0), reverse=True)
    for i, (user_id, data) in enumerate(sorted_users):
        if user_id == str(uid) and i > 0:
            mouse = sorted_users[i-1][1]
            diff = mouse.get('total_score', 0) - data.get('total_score', 0)
            mouse_name = mouse.get('info', {}).get('nickname', 'Raqib')
            return f"Siz '{mouse_name}'dan {diff} ball orqada ketyapsiz! 🐁💨"
    return "Siz hozircha peshqadamsiz! 🏆"

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    web_url = "https://muminbaevshohjahon-bit.github.io/telegram-bot/" 
    markup.add(KeyboardButton("Kabinet 📱", web_app=WebAppInfo(url=web_url)))
    markup.add(KeyboardButton("Peshqadamlar 🏆"), KeyboardButton("Finish 🏁"))
    return markup

# --- LOGIKA ---
@bot.message_handler(commands=['start'])
def start(message):
    user = get_user(message.chat.id)
    if user.get('step') == 'main':
        bot.send_message(message.chat.id, "Yana xush kelibsiz!", reply_markup=main_menu())
    else:
        welcome = (
            "<b>Assalomu aleykum xush kelibsiz!</b>\n"
            "Men MBE useful tomonidan yaratilgan botman!\n\n"
            "Maqsadimiz 30 kunlik chellenj davomida intizomni shakllantirish.\n"
            "Keling tanishib olaylik... <b>Ismingizni kiriting:</b>"
        )
        user['step'] = 'wait_name'
        save_data()
        bot.send_message(message.chat.id, welcome, parse_mode='HTML')

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'wait_name')
def register(message):
    user = get_user(message.chat.id)
    user['info']['nickname'] = message.text
    user['info']['public_id'] = f"MBE-{random.randint(1000, 9999)}"
    user['step'] = 'main'
    save_data()
    bot.send_message(message.chat.id, f"Zo'r! {message.text}, ro'yxatdan o'tdingiz. 🔥", reply_markup=main_menu())

@bot.message_handler(content_types=['web_app_data'])
def web_app_receive(message):
    data = json.loads(message.web_app_data.data)
    user = get_user(message.chat.id)
    
    # Bugun Finish bosilganmi?
    today = datetime.now().strftime('%d/%m')
    if any(today in entry for entry in user['history']):
        bot.send_message(message.chat.id, "Bugun yakunlangan! Ertaga ko'rishamiz. 👋")
        return

    if data.get('action') == "done":
        task = data.get('task')
        if task not in user['completed_today']:
            user['completed_today'].append(task)
            user['total_score'] += 10
            save_data()
            bot.send_message(message.chat.id, f"✅ {task} bajarildi!\n\n{random.choice(CUSTOM_MOTIVATIONS)}")

@bot.message_handler(func=lambda m: m.text == "Peshqadamlar 🏆")
def show_leaderboard(message):
    sorted_u = sorted(user_data.items(), key=lambda x: x[1].get('total_score', 0), reverse=True)[:10]
    text = "🏆 <b>TOP 10 PESHQADAMLAR</b>\n\n"
    for i, (uid, data) in enumerate(sorted_u):
        name = data.get('info', {}).get('nickname', 'User')
        text += f"{i+1}. {name} — {data.get('total_score', 0)} ball\n"
    text += f"\n{get_mouse_info(message.chat.id)}"
    bot.send_message(message.chat.id, text, parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "Finish 🏁")
def finish_day(message):
    user = get_user(message.chat.id)
    today = datetime.now().strftime('%d/%m')
    
    if any(today in entry for entry in user['history']):
        bot.send_message(message.chat.id, "Bugun allaqachon yakunlangan! 👋")
        return

    percent = int((len(user['completed_today']) / TOTAL_TASKS) * 100)
    user['history'].append(f"{today}: {percent}%")
    user['completed_today'] = []
    save_data()
    
    msg = f"🏁 <b>Natija: {percent}%</b>\n\n{random.choice(FINISH_MOTIVATIONS)}\n\n{get_mouse_info(message.chat.id)}"
    bot.send_animation(message.chat.id, random.choice(GIFS), caption=msg, parse_mode='HTML')

# --- ESLATMALAR VA AUTO-FINISH ---
def scheduler():
    while True:
        now = datetime.now().strftime("%H:%M")
        # Motivatsiya (09:00, 14:00, 19:00)
        if now in ["09:00", "14:00", "19:00"]:
            for uid in list(user_data.keys()):
                try: bot.send_message(uid, f"💡 <b>Eslatma:</b>\n\n{random.choice(CUSTOM_MOTIVATIONS)}")
                except: pass
        
        # Avto Finish (23:30)
        if now == "23:30":
            for uid, data in user_data.items():
                if data.get('completed_today'):
                    p = int((len(data['completed_today']) / TOTAL_TASKS) * 100)
                    data['history'].append(f"{datetime.now().strftime('%d/%m')}: {p}% (Auto)")
                    data['completed_today'] = []
                    bot.send_message(uid, f"⏰ <b>Finish unutildi!</b>\nBugungi natija: {p}%")
            save_data()
        time.sleep(60)

threading.Thread(target=scheduler, daemon=True).start()

bot.infinity_polling()
