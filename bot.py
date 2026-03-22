import telebot
import os
import random
import threading
import time
import json
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# --- DATA PERSISTENCE ---
def save_data():
    with open('users_db.json', 'w') as f:
        json.dump(user_data, f)

def load_data():
    if os.path.exists('users_db.json'):
        with open('users_db.json', 'r') as f:
            try: return json.load(f)
            except: return {}
    return {}

user_data = load_data()

DAILY_TASKS = [
    "Tongda detox (1 soat) 📵", "Kitob mutolasi 📚", "Sugar detox 🍬",
    "Gazsiz ichimliklar 🥤", "5000 so'm sarmoya 💰", "Jismoniy mashq 💪",
    "1 daqiqa hech narsa qilmaslik 🧘‍♂️"
]

# --- SIZ BERGAN 100 TA MOTIVATSIYA ---
MOTIVATIONS = [
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
    "Sen hech qachon yolg‘iz emassan — o‘zing bor.", "Boshlagin. Hozir. Shu yerda."
]

GIFS = [
    "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3eXJqM3Z4eXp5bmZ6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6JmR6PTEmZ3R6Z3R6/3o7TKDkDbIDJieKbVm/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOTVkZ3hueXBnNjkwZ2J1YjJkN2gwMHN3b3M3aXZ0cnRvMDFpbHdkZyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/FACfMgP1N9mlG/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3eTZjbDQ0NjhqdmY5ZnJ5eDdqY2pvcHN2c21yMjZ3OHExcHdlanN0ayZlcD12MV9naWZzX3NlYXJjaCZjdD1n/XMnjfm65r82TirNhoe/giphy.gif"
]

# --- HELPERS ---
def get_user(uid):
    uid = str(uid)
    if uid not in user_data:
        user_data[uid] = {
            'info': {}, 'daily_count': 0, 'history': [],
            'total_score': 0, 'completed_tasks': [], 'step': 'start'
        }
    return user_data[uid]

def main_menu():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(KeyboardButton("Bugungi vazifalar ✅"), KeyboardButton("Natijalar jadvali 🏆"))
    markup.add(KeyboardButton("Reyting 📊"), KeyboardButton("Finish 🏁"))
    return markup

# --- REGISTRATION ---
@bot.message_handler(commands=['start'])
def start(message):
    uid = str(message.chat.id)
    user = get_user(uid)
# --- REGISTRATION (TAYYOR VA TUZATILGAN VARIANT) ---
@bot.message_handler(commands=['start'])
def start(message):
    uid = str(message.chat.id)
    user = get_user(uid)
    
    # 1. Siz so'ragan formatlangan matn
    welcome_text = (
        "<b><i>Assalomu aleykum hush kelibsiz!</i></b>\n"
        "<b><i>Men MBE useful tomonidan yaratilgan botman!</i></b>\n\n"
        "<b><i>Maqsadimiz 30 kunlik chellenj davomida intizomni shakllantirish.</i></b>\n"
        "<b><i>Balki foydasi tegar...</i></b>\n\n"
        "Keling tanishib olaylik... Ismingizni kiriting:"
    )
    
    # 2. Foydalanuvchi holatini yangilash
    user['step'] = 'get_name'
    save_data()
    
    # 3. Matnni foydalanuvchiga yuborish
    bot.send_message(uid, welcome_text, parse_mode='HTML')

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
    bot.send_message(message.chat.id, "Tug‘ilgan oy (1-12):")

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_month')
def get_month(message):
    user = get_user(message.chat.id)
    user['info']['birth_month'] = message.text
    user['step'] = 'get_day'
    save_data()
    bot.send_message(message.chat.id, "Tug‘ilgan kun (1-31):")

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_day')
def get_day(message):
    user = get_user(message.chat.id)
    user['info']['birth_day'] = message.text
    user['step'] = 'get_nick'
    save_data()
    bot.send_message(message.chat.id, "Nickname kiriting:")

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_nick')
def get_nick(message):
    user = get_user(message.chat.id)
    user['info']['nickname'] = message.text
    user['step'] = 'main'
    public_id = f"MBE-{random.randint(10000, 99999)}"
    user['info']['public_id'] = public_id
    save_data()
    bot.send_message(message.chat.id, f"Tabrikleyshn ro‘yxatdan o‘tdingiz! ID: <b>{public_id}</b>", parse_mode='HTML', reply_markup=main_menu())
# --- TASKS ---
@bot.message_handler(func=lambda m: m.text == "Bugungi vazifalar ✅")
def show_tasks(message):
    user = get_user(message.chat.id)
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for task in DAILY_TASKS:
        prefix = "✅ " if task in user.get('completed_tasks', []) else ""
        markup.add(KeyboardButton(f"{prefix}{task}"))
    markup.add(KeyboardButton("Orqaga ⬅️"))
    bot.send_message(message.chat.id, f"Holat: {user['daily_count']}/{len(DAILY_TASKS)}", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in DAILY_TASKS or (m.text.startswith("✅ ") and m.text[2:] in DAILY_TASKS))
def complete_task(message):
    user = get_user(message.chat.id)
    task_name = message.text.replace("✅ ", "")
    if task_name in user.get('completed_tasks', []):
        bot.send_message(message.chat.id, "Bajarilgan!")
        return
    user.setdefault('completed_tasks', []).append(task_name)
    user['daily_count'] += 1
    user['total_score'] += 10
    save_data()
    bot.send_message(message.chat.id, f"✅ +10 ball\n{random.choice(MOTIVATIONS)}")

# --- FINISH (RANDOM GIF + MOTIVATSIYA) ---
@bot.message_handler(func=lambda m: m.text == "Finish 🏁")
def finish_day(message):
    user = get_user(message.chat.id)
    if user['daily_count'] == 0:
        bot.send_message(message.chat.id, "Hech bo'lmasa bitta vazifa bajaring!")
        return

    percent = int((user['daily_count'] / len(DAILY_TASKS)) * 100)
    user['history'].append(f"{datetime.now().strftime('%d/%m')} - {percent}%")
    
    # Random motivatsiya va GIF
    motivation = random.choice(MOTIVATIONS)
    gif = random.choice(GIFS)
    
    bot.send_animation(message.chat.id, gif, caption=f"🏁 <b>Kun yakunlandi!</b>\nNatija: {percent}%\n\n<i>{motivation}</i>", parse_mode='HTML')

    user['daily_count'] = 0
    user['completed_tasks'] = []
    save_data()

# --- OTHER MENUS ---
@bot.message_handler(func=lambda m: m.text == "Reyting 📊")
def show_rank(message):
    sorted_u = sorted(user_data.items(), key=lambda x: x[1]['total_score'], reverse=True)[:10]
    text = "🏆 <b>TOP 10</b>\n\n"
    for i, (uid, data) in enumerate(sorted_u):
        text += f"{i+1}. {data['info'].get('nickname', 'User')} — {data['total_score']} ball\n"
    bot.send_message(message.chat.id, text, parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "Natijalar jadvali 🏆")
def show_results(message):
    user = get_user(message.chat.id)
    history = "\n".join(user['history']) if user['history'] else "Hali natijalar yo'q."
    bot.send_message(message.chat.id, f"📊 <b>Sizning tarixingiz:</b>\n{history}", parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "Orqaga ⬅️")
def back(message):
    bot.send_message(message.chat.id, "Menyu:", reply_markup=main_menu())

# --- RANDOM REMINDER SYSTEM (KUN DAVOMIDA) ---
def reminder_loop():
    while True:
        now = datetime.now().hour
        # Kun davomida (09:00 dan 22:00 gacha) har soatda random motivatsiya
        if 9 <= now <= 22:
            for uid in list(user_data.keys()):
                try:
                    if user_data[uid].get('step') == 'main':
                        bot.send_message(uid, f"💡 <b>Kunlik motivatsiya:</b>\n\n{random.choice(MOTIVATIONS)}", parse_mode='HTML')
                except:
                    pass
        time.sleep(3600) # 1 soat kutish

threading.Thread(target=reminder_loop, daemon=True).start()

# --- RUN ---
bot.infinity_polling()

