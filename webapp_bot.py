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

# Motivatsiyalar (Siz yozgan ro'yxat)
CUSTOM_MOTIVATIONS = [
    "Sen boshlamasang, hech narsa boshlanmaydi. 🔥",
    "Bugungi og‘riq — ertangi kuch. 💪",
    "Eng zo‘r vaqt — hozir. 🚀",
    "Intizom — bu o'ziga berilgan va'dani bajarishdir. ✨",
    "Har kuni kichik qadam — katta natija.",
    "Eng katta raqibing — kechagi o‘zing."
]

FINISH_MOTIVATIONS = [
    "Dahshat! Vapshe zo'r, barakalla! 🔥",
    "Sen o'ylagandan ham kuchlisan, davom et! 💪",
    "Intizom — bu o'zingga bo'lgan hurmat. 🌟"
]

GIFS = ["https://media.giphy.com/media/FACfMgP1N9mlG/giphy.gif"]

def get_user(uid):
    uid = str(uid)
    if uid not in user_data:
        user_data[uid] = {'total_score': 0, 'history': [], 'completed_today': [], 'info': {}, 'step': 'start'}
    return user_data[uid]

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    web_url = "https://muminbaevshohjahon-bit.github.io/telegram-bot/" 
    markup.add(KeyboardButton("Kabinet 📱", web_app=WebAppInfo(url=web_url)))
    markup.add(KeyboardButton("Peshqadamlar 🏆"), KeyboardButton("Finish 🏁"))
    return markup

# --- LOGIKA ---
@bot.message_handler(commands=['start'])
def start(message):
    user = get_user(message.chat.id)
    text = "<b>Assalomu alaykum!</b>\nKeling tanishib olamiz!\n<b>Ismingiz:</b>"
    user['step'] = 'get_name'
    save_data()
    bot.send_message(message.chat.id, text, parse_mode='HTML')

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
    bot.send_message(message.chat.id, f"Muvaffaqiyatli ro'yxatdan o'tdingiz!\nSizning ID: <b>{pid}</b>", parse_mode='HTML', reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == "Peshqadamlar 🏆")
def leaderboard(message):
    sorted_u = sorted(user_data.items(), key=lambda x: x[1].get('total_score', 0), reverse=True)[:10]
    text = "🏆 <b>TOP 10 PESHQADAMLAR</b>\n\n"
    for i, (uid, data) in enumerate(sorted_u):
        nick = data.get('info', {}).get('nickname', "Mehmon")
        pid = data.get('info', {}).get('public_id', "ID-yo'q")
        score = data.get('total_score', 0)
        text += f"{i+1}. {nick} [{pid}] — {score} ball\n"
    bot.send_message(message.chat.id, text, parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "Finish 🏁")
def finish_day(message):
    user = get_user(message.chat.id)
    today = datetime.now().strftime('%d/%m')
    if any(today in entry for entry in user['history']):
        bot.send_message(message.chat.id, "Bugun uchun vazifalar yakunlangan. ✨")
        return
    percent = int((len(user['completed_today']) / TOTAL_TASKS) * 100)
    user['history'].append(f"{today}: {percent}%")
    user['completed_today'] = []
    save_data()
    msg = f"🏁 <b>Natija: {percent}%</b>\n\n{random.choice(FINISH_MOTIVATIONS)}"
    bot.send_message(message.chat.id, msg, parse_mode='HTML')

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
            bot.send_message(message.chat.id, f"✅ {task} bajarildi!\n{random.choice(CUSTOM_MOTIVATIONS)}")

if __name__ == "__main__":
    bot.infinity_polling()
