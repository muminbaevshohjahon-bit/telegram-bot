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

# 1. TO'LIQ CUSTOM MOTIVATIONS (Vazifa bajarilganda)
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

# 2. TO'LIQ FINISH MOTIVATIONS (50% dan oshganda)
FINISH_MOTIVATIONS = [
    "Dahshat! Vapshe zo'r, barakalla! 🔥",
    "Sen o'ylagandan ham kuchlisan, davom et! 💪",
    "Intizom — bu o'zingga bo'lgan hurmat. 🌟",
    "Bo'lar ekanku, senga ishonaman!",
    "Bo'shashma zo'r ketayabsan",
    "Ko'zim to'rt bo'lib ketdi, malades."
]

# 3. TO'LIQ GIF LINKLARI
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
    web_url = f"https://muminbaevshohjahon-bit.github.io/telegram-bot/?v={random.randint(1, 999)}"
    markup.add(KeyboardButton("Chellenjlar 🗓", web_app=WebAppInfo(url=web_url)))
    markup.add(KeyboardButton("Peshqadamlar 🏆"), KeyboardButton("Mening natijam 📊"))
    markup.add(KeyboardButton("Finish 🏁"))
    return markup

# --- PESHQADAMLAR (SOLISHTIRISH BILAN) ---
@bot.message_handler(func=lambda m: m.text == "Peshqadamlar 🏆")
def leaderboard(message):
    users = []
    for uid, data in user_data.items():
        if 'info' in data and 'nickname' in data['info']:
            users.append({'nick': data['info']['nickname'], 'score': data.get('total_score', 0), 'uid': uid})
    
    if not users:
        bot.send_message(message.chat.id, "Hali hech kim yo'q.")
        return

    users.sort(key=lambda x: x['score'], reverse=True)
    top_user = users[0]
    my_uid = str(message.chat.id)
    my_score = get_user(my_uid).get('total_score', 0)

    text = "🏆 <b>Eng kuchli ishtirokchilar:</b>\n\n"
    for i, u in enumerate(users[:10], 1):
        text += f"{i}. {u['nick']} — {u['score']} ball\n"

    if top_user['uid'] != my_uid:
        diff = top_user['score'] - my_score
        p_diff = int((diff / my_score * 100)) if my_score > 0 else 100
        text += f"\n\n💡 <b>Solishtirish:</b>\n{top_user['nick']} sendan {p_diff}% kuchliroq! Uni quvib o'tishga harakat qil! 🔥"
    
    bot.send_message(message.chat.id, text, parse_mode='HTML')

# --- FINISH VA 30-KUN ---
@bot.message_handler(func=lambda m: m.text == "Finish 🏁")
def finish_day(message):
    user = get_user(message.chat.id)
    today = datetime.now().strftime('%d/%m')
    
    if any(today in entry for entry in user.get('history', [])):
        bot.send_message(message.chat.id, "Bugun yakunlab bo'lingan! ✨")
        return

    percent = int((len(user.get('completed_today', [])) / TOTAL_TASKS) * 100)
    user.setdefault('history', []).append(f"{today}: {percent}%")
    user['completed_today'] = [] 
    save_data()

    if len(user.get('history', [])) == 30:
        bot.send_animation(message.chat.id, "https://media.giphy.com/media/g9582DNuQppxC/giphy.gif", 
                           caption="🎉 <b>URRAA! 30 KUN YAKUNLANDI!</b> 🎉\nSiz haqiqiy g'olibsiz! 🏆", parse_mode='HTML')
        return

    if percent <= 20: motivation = "Sen qo'lingdan kelganini qilding, ishonaman bundan ko'piga loyiqsan. Ertaga kuchliroq bo'lib qaytasan!"
    elif percent <= 30: motivation = "Senga ishonaman, ertaga ko'proqini uddalaysan. Muhimi sen to'xtab qolmading!"
    elif percent <= 50: motivation = "Bilardim uddalay olishingni, oz qoldi!"
    else: motivation = random.choice(FINISH_MOTIVATIONS)

    msg = f"🏁 <b>Natija: {percent}%</b>\n\n{motivation}"
    try: bot.send_animation(message.chat.id, random.choice(GIFS), caption=msg, parse_mode='HTML')
    except: bot.send_message(message.chat.id, msg, parse_mode='HTML')

# --- START VA RO'YXATDAN O'TISH ---
@bot.message_handler(commands=['start'])
def start(message):
    uid = str(message.chat.id)
    user_data[uid] = {'total_score': 0, 'history': [], 'completed_today': [], 'info': {}, 'step': 'get_name'}
    save_data()
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
    uid = str(message.chat.id)
    user_data[uid]['info']['name'] = message.text
    user_data[uid]['step'] = 'get_birth'
    save_data()
    bot.send_message(message.chat.id, "Tug‘ilgan yilingiz:")

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_birth')
def get_birth(message):
    uid = str(message.chat.id)
    user_data[uid]['info']['birth_year'] = message.text
    user_data[uid]['step'] = 'get_nick'
    save_data()
    bot.send_message(message.chat.id, "Nickname kiriting:")

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_nick')
def get_nick(message):
    uid = str(message.chat.id)
    user_data[uid]['info']['nickname'] = message.text
    user_data[uid]['step'] = 'main'
    save_data()
    bot.send_message(message.chat.id, "Ro'yxatdan o'tildi!", reply_markup=main_menu())

# --- MENING NATIJAM ---
@bot.message_handler(func=lambda m: m.text == "Mening natijam 📊")
def my_stats(message):
    user = get_user(message.chat.id)
    history = user.get('history', [])
    stat_text = "📊 <b>Natijalar:</b>\n\n"
    if not history: stat_text += "Hali natija yo'q."
    else:
        for entry in history[-7:]:
            day, res = entry.split(": ")
            icon = "✅" if "100" in res else "📈"
            stat_text += f"{icon} {day}: {res}\n"
    stat_text += f"\n🔥 Umumiy ball: {user.get('total_score', 0)}"
    bot.send_message(message.chat.id, stat_text, parse_mode='HTML')

# --- NOTIFICATIONS (ESLATMALAR) ---
def auto_scheduler():
    while True:
        now = datetime.now().strftime("%H:%M")
        if now == "08:00":
            for uid in user_data.keys():
                try: bot.send_message(uid, "☀️ Xayrli tong! Chellenjlarni boshlaymizmi?")
                except: pass
            time.sleep(61)
        if now == "21:00":
            for uid in user_data.keys():
                try: bot.send_message(uid, "🔔 Finish tugmasini bosish esdan chiqmadimi?")
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
