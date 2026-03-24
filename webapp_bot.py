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
CHANNEL_ID = "@caffeinefan"  # Kanal username yoki ID

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

# MOTIVATSIYA
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
    "O‘zgarish sendan boshlanadi.", "Boshlagin. Hozir. Shu yerda.",
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


# --- HELPER FUNCTIONS ---
def get_user(uid):
    uid = str(uid)
    if uid not in user_data:
        user_data[uid] = {'total_score': 0, 'history': [], 'completed_today': [], 'info': {}, 'step': 'start'}
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
        if member.status in ['creator', 'administrator', 'member']:
            return True
        else:
            return False
    except:
        return False

# --- START VA REGISTRATSIYA ---
@bot.message_handler(commands=['start'])
def start(message):
    uid = message.chat.id
    user = get_user(uid)
    
    # Kanalga obuna bo'lish tekshiruvi
    if not check_subscription(uid):
        bot.send_message(uid, f"⚠️ Botdan foydalanish uchun kanalimizga obuna bo‘ling: {CHANNEL_ID}\n\nObuna bo‘lganingizdan so‘ng /start qayta bosing.")
        user['step'] = 'waiting_subscription'
        save_data()
        return

    # Agar foydalanuvchi avvaldan ro'yxatdan o'tgan bo'lsa
    if user['step'] == 'main':
        bot.send_message(uid, "Siz allaqachon ro'yxatdan o'tgansiz!", reply_markup=main_menu())
        return

    # Ro'yxatdan boshlash
    user['step'] = 'get_name'
    user['info'] = {}  # info bo'shatamiz, yangi start
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
    bot.send_message(message.chat.id, "Nickname kiriting:")

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_nick')
def get_nick(message):
    uid = str(message.chat.id)
    user_data[uid]['info']['nickname'] = message.text
    user_data[uid]['step'] = 'main'
    save_data()
    bot.send_message(message.chat.id, "Tabriklayman, ro'yxatdan o'tdingiz!🔥", reply_markup=main_menu())

# --- ADMIN PANEL ---
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
            info = data.get('info', {})
            name = info.get('name', "Noma'lum")
            nick = info.get('nickname', "Yo'q")
            day = info.get('birth_day', "??")
            month = info.get('birth_month', "??")
            year = info.get('birth_year', "????")
            score = data.get('total_score', 0)
            text += f"👤 {name} (@{nick}) — {score} ball\n🎂 {day}/{month}/{year}\n🆔 {uid}\n\n"
        bot.send_message(message.chat.id, text, parse_mode='HTML')

@bot.message_handler(commands=['db_download'])
def send_db(message):
    if message.chat.id == ADMIN_ID:
        try:
            with open('users_db.json', 'rb') as f:
                bot.send_document(message.chat.id, f)
        except:
            bot.send_message(message.chat.id, "Baza fayli topilmadi.")

# --- LEADERBOARD ---
@bot.message_handler(func=lambda m: m.text == "Peshqadamlar 🏆")
def leaderboard(message):
    users = []
    for uid, data in user_data.items():
        score = data.get('total_score', 0)
        nick = data.get('info', {}).get('nickname', "Yo'q")
        users.append({'uid': uid, 'score': score, 'nick': nick})

    users.sort(key=lambda x: x['score'], reverse=True)
    if not users:
        bot.send_message(message.chat.id, "Hozircha hech kim ball to'plamadi.")
        return

    text = "🏆 <b>Eng kuchli ishtirokchilar:</b>\n\n"
    for i, u in enumerate(users[:10], 1):
        text += f"{i}. {u['nick']} — {u['score']} ball\n"
    bot.send_message(message.chat.id, text, parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "Mening natijam 📊")
def my_result(message):
    uid = str(message.chat.id)
    if uid not in user_data:
        bot.send_message(uid, "Siz hali ro'yxatdan o'tmagansiz. /start bosing.")
        return

    data = user_data[uid]
    info = data.get('info', {})
    name = info.get('name', "Noma'lum")
    score = data.get('total_score', 0)
    day = info.get('birth_day', "??")
    month = info.get('birth_month', "??")
    year = info.get('birth_year', "????")
    current_day = data.get('current_day', 1)

    response_text = f"""📊 **Sizning natijangiz:**
👤 {name}
🆔 `{uid}`
🎂 {day}/{month}/{year}
⭐ {score} ball
📅 Hozirgi kun: **{current_day}-kun**
"""
    bot.send_message(uid, response_text, parse_mode='Markdown')

# --- FINISH ---
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

    if percent >= 50:
        motivation = random.choice(FINISH_MOTIVATIONS)
        bot.send_animation(message.chat.id, random.choice(GIFS), caption=f"🏁 Natija: {percent}%\n\n{motivation}", parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, f" Natija: {percent}%\n\nErtaga kuchliroq bo'lamiz! 💪", parse_mode='HTML')

# --- SCHEDULER ---
def auto_scheduler():
    threading.Thread(target=check_subscription_periodically, daemon=True).start()
    while True:
        now = datetime.now().strftime("%H:%M")
        if now == "08:00":
            for uid in list(user_data.keys()):
                try:
                    bot.send_message(uid, "☀️ Xayrli tong! Bugun 7 ta vazifani ham bajaramizmi?")
                except: pass
            time.sleep(61)
        if now == "21:00":
            for uid in list(user_data.keys()):
                try:
                    bot.send_message(uid, "🔔 Kun yakunlanmoqda, Finish tugmasini bosishni unutmang!")
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

threading.Thread(target=check_subscription_periodically, daemon=True).start()

# --- WEBAPP ---
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

            percent = int((len(user['completed_today']) / TOTAL_TASKS) * 100)
            if percent >= 20:
                bot.send_animation(
                    message.chat.id,
                    random.choice(GIFS),
                    caption=f"🔥 {task} bajarildi!\n+10 ball\n\n{random.choice(CUSTOM_MOTIVATIONS)}",
                    parse_mode='HTML'
                )
            else:
                bot.send_message(
                    message.chat.id,
                    f"✅ {task} bajarildi!\n+10 ball\n\n{random.choice(CUSTOM_MOTIVATIONS)}"
                )
# --- SUBSCRIPTION CHECKER ---
def check_subscription_periodically():
    while True:
        for uid, user in user_data.items():
            if user.get('step') == 'waiting_subscription':
                if check_subscription(uid):
                    user['step'] = 'get_name'
                    save_data()
                    bot.send_message(uid, "🎉 Rahmat! Endi botdan foydalana olasiz!")
                    rules_text = (
                        "📜 <b>Qoidalar:</b>\n\n"
                        "Botga start bosib registratsiyadan so‘ng chellenjni boshlash mumkin.\n\n"
                        "1) Kitob mutolaasi\n"
                        "2) Jismoniy mashq\n"
                        "3) Shakarsiz hayot\n"
                        "4) 5000 so‘mdan sarmoya\n"
                        "5) Gazsiz ichimlik\n"
                        "6) Tongda detoks\n"
                        "7) 2 daqiqa sukunat\n"
                        "8) DEEP WORK (chalg'imasdan 25 daqiqa ishlash)\n\n"
                        "Xamma topshiriq sodda, minimalini bajarish talab qilinadi. "
                        "Jismoniy mashq – har qanday yurish yoki 10 ta otdjimaniya, "
                        "detoks – uyg‘ongach kamida 1 soat telefonni ishlatmang, "
                        "sarmoya – kuniga 5000 so‘m, yig‘ing yoki IMAN omonatiga qo‘ying.\n\n"
                        "Biz sizni toqatingizdan ortig‘iga majbur qilmaymiz 😊"
                    )
                    bot.send_message(uid, rules_text, parse_mode='HTML')
        time.sleep(10)  # har 10 soniyada tekshiradi
        
if __name__ == "__main__":
    bot.infinity_polling()
