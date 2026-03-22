import telebot
import os
import random
import json
import threading
import time
from datetime import datetime
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# Ma'lumotlar bazasi
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
TOTAL_TASKS = 7 # Jami vazifalar soni

MOTIVATIONS = [    "Sen boshlamasang, hech narsa boshlanmaydi.", "Mukammallikni kutma — harakatni boshlash muhim.",
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
    "Sen hech qachon yolg‘iz emassan — o‘zing bor.", "Boshlagin. Hozir. Shu yerda.
    "Dahshat! Vapshe zo'r, barakalla! 🔥",
    "Sen o'ylagandan ham kuchlisan, davom et! 💪",
    "Intizom — bu o'zingga bo'lgan hurmat. Zo'r ketyapsan! 🌟",
    "Bugun kechagidan yaxshiroq bo'lding. Ofarin! 👏"
]

GIFS = [
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaXU3bGl0dXg3c3FxM3VuZnl1ZW8wamRlbW5vbncxN2V1enNoNjhxOCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/8ZblO3ZD5NMltPaFS2/giphy.gif",
    "https://media.giphy.com/media/FACfMgP1N9mlG/giphy.gif"
]

def get_user(uid):
    uid = str(uid)
    if uid not in user_data:
        user_data[uid] = {
            'total_score': 0, 
            'history': [], 
            'completed_today': [], 
            'info': {'nickname': f"User_{uid[-4:]}", 'public_id': f"MBE-{random.randint(1000, 9999)}"}
        }
    return user_data[uid]

def get_mouse_info(uid):
    """Foydalanuvchidan bir pog'ona yuqoridagi 'Sichqoncha'ni aniqlash"""
    sorted_users = sorted(user_data.items(), key=lambda x: x[1]['total_score'], reverse=True)
    for i, (user_id, data) in enumerate(sorted_users):
        if user_id == str(uid) and i > 0:
            mouse = sorted_users[i-1][1]
            diff = mouse['total_score'] - data['total_score']
            return f"Siz '{mouse['info']['nickname']}'dan {diff} ball orqada ketyapsiz! 🐁💨"
    return "Siz hozircha peshqadamsiz! 🏆"

# --- WEB APP DATA ---
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
            bot.send_message(message.chat.id, f"✅ {task} bajarildi!\n\n{random.choice(MOTIVATIONS)}")

# --- BUTTONS ---
@bot.message_handler(func=lambda m: m.text == "Peshqadamlar 🏆")
def show_leaderboard(message):
    sorted_u = sorted(user_data.items(), key=lambda x: x[1]['total_score'], reverse=True)[:10]
    text = "🏆 <b>TOP 10 PESHQADAMLAR</b>\n\n"
    for i, (uid, data) in enumerate(sorted_u):
        status = "⭐" if i < 3 else "🔹"
        text += f"{status} {i+1}. {data['info']['nickname']} (ID: {data['info']['public_id']}) — {data['total_score']} ball\n"
    
    text += f"\n👉 {get_mouse_info(message.chat.id)}"
    bot.send_message(message.chat.id, text, parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "Finish 🏁")
def finish_day(message):
    user = get_user(message.chat.id)
    percent = int((len(user['completed_today']) / TOTAL_TASKS) * 100)
    today = datetime.now().strftime('%d/%m')
    
    user['history'].append(f"{today}: {percent}%")
    user['completed_today'] = []
    save_data()
    
    msg = f"🏁 <b>Kun yakunlandi! Natija: {percent}%</b>\n\n{random.choice(MOTIVATIONS)}\n\n{get_mouse_info(message.chat.id)}"
    bot.send_animation(message.chat.id, random.choice(GIFS), caption=msg, parse_mode='HTML')

# --- AVTOMATIK MOTIVATSIYA VA FINISH (Reminder) ---
def scheduler():
    while True:
        now = datetime.now().strftime("%H:%M")
        # Motivatsiya soatlari
        if now in ["09:00", "14:00", "19:00"]:
            for uid in list(user_data.keys()):
                try: bot.send_message(uid, f"💡 <b>Eslatma:</b>\n\n{random.choice(MOTIVATIONS)}", parse_mode='HTML')
                except: pass
        
        # Avtomatik Finish (Soat 23:30 da)
        if now == "23:30":
            for uid, data in user_data.items():
                if data['completed_today']:
                    # Finish funksiyasini avtomatik ishlatish
                    percent = int((len(data['completed_today']) / TOTAL_TASKS) * 100)
                    data['history'].append(f"{datetime.now().strftime('%d/%m')}: {percent}% (Auto)")
                    data['completed_today'] = []
                    bot.send_message(uid, f"⏰ <b>Finish unutildi!</b>\nAvtomatik hisoblandi: {percent}%\n\n{get_mouse_info(uid)}", parse_mode='HTML')
            save_data()
        
        time.sleep(60)

threading.Thread(target=scheduler, daemon=True).start()

# Asosiy menyu tugmalari
@bot.message_handler(commands=['start'])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    web_url = "https://muminbaevshohjahon-bit.github.io/telegram-bot/" 
    markup.add(KeyboardButton("Kabinet 📱", web_app=WebAppInfo(url=web_url)))
    markup.add(KeyboardButton("Peshqadamlar 🏆"), KeyboardButton("Finish 🏁"))
    bot.send_message(message.chat.id, "MBE Useful botiga xush kelibsiz!", reply_markup=markup)

bot.infinity_polling()
