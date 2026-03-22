import telebot
import os
import random
import threading
import time
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime

TOKEN = os.getenv("TOKEN") or "YOUR_BOT_TOKEN"
bot = telebot.TeleBot(TOKEN)

# --- DATA ---
user_data = {}

DAILY_TASKS = [
    "Tongda detox (1 soat) 📵",
    "Kitob mutolasi 📚",
    "Sugar detox 🍬",
    "Gazsiz ichimliklar 🥤",
    "5000 so'm sarmoya 💰",
    "Jismoniy mashq 💪",
    "1 daqiqa hech narsa qilmaslik 🧘‍♂️"
]

MOTIVATIONS = [
    "Sen boshlamasang, hech narsa boshlanmaydi.",
    "Bugungi og‘riq — ertangi kuch.",
    "Eng katta raqibing — kechagi o‘zing.",
    "Har kuni kichik qadam — katta natija.",
    "Eng yaxshi vaqt — hozir."
]

GIFS = [
    "https://media.giphy.com/media/3o7TKDkDbIDJieKbVm/giphy.gif",
    "https://media.giphy.com/media/FACfMgP1N9mlG/giphy.gif",
    "https://media.giphy.com/media/XMnjfm65r82TirNhoe/giphy.gif",
    "https://media.giphy.com/media/x4dS8uOkeEFdxvV1nz/giphy.gif",
]

REMINDERS = {
    "morning": [
        "Hoy qayerdasan? Tur o'rningdan! 🏃‍♂️",
        "Bugun o'zingni yengish kuni! ✨"
    ],
    "afternoon": [
        "Qani bo'la qoling... vazifalar qolib ketmasin! 🥗",
        "Kitob o‘qimayapsizmi? 😉 📖"
    ],
    "evening": [
        "Hali imkoniyat bor! 🔥",
        "Uxlashdan oldin vazifalarni yopamiz! 🎫"
    ]
}

# --- HELPERS ---
def get_user(uid):
    if uid not in user_data:
        user_data[uid] = {
            'info': {},
            'daily_count': 0,
            'history': [],
            'total_score': 0,
            'completed_tasks': [],
            'step': 'start'
        }
    return user_data[uid]

def main_menu():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add(
        KeyboardButton("Bugungi vazifalar ✅"),
        KeyboardButton("Natijalar jadvali 🏆"),
        KeyboardButton("Reyting 📊"),
        KeyboardButton("Finish 🏁")
    )
    return markup

# --- REGISTER ---
@bot.message_handler(commands=['start'])
def start(message):
    user = get_user(message.chat.id)
    user['step'] = 'get_name'

    bot.send_message(message.chat.id,
        "<b>Assalomu alaykum!</b>\nIsmingizni kiriting:",
        parse_mode='HTML'
    )

@bot.message_handler(func=lambda m: get_user(m.chat.id)['step']=='get_name')
def get_name(message):
    user = get_user(message.chat.id)
    user['info']['name'] = message.text
    user['step'] = 'get_birth'

    bot.send_message(message.chat.id, "Tug‘ilgan yil (2003):")

@bot.message_handler(func=lambda m: get_user(m.chat.id)['step']=='get_birth')
def get_birth(message):
    if not message.text.isdigit():
        bot.send_message(message.chat.id, "Faqat yil kiriting!")
        return

    user = get_user(message.chat.id)
    user['info']['birth_year'] = message.text
    user['step'] = 'get_month'

    bot.send_message(message.chat.id, "Tug‘ilgan oy (1-12):")

@bot.message_handler(func=lambda m: get_user(m.chat.id)['step']=='get_month')
def get_month(message):
    if not message.text.isdigit() or not 1 <= int(message.text) <= 12:
        bot.send_message(message.chat.id, "1-12 kiriting!")
        return

    user = get_user(message.chat.id)
    user['info']['birth_month'] = message.text
    user['step'] = 'get_nick'

    bot.send_message(message.chat.id, "Nickname kiriting:")

@bot.message_handler(func=lambda m: get_user(m.chat.id)['step']=='get_nick')
def get_nick(message):
    user = get_user(message.chat.id)

    user['info']['nickname'] = message.text
    user['step'] = 'main'

    # PUBLIC ID
    public_id = f"USER-{random.randint(10000,99999)}"
    user['info']['public_id'] = public_id

    bot.send_message(message.chat.id,
        f"Ro‘yxatdan o‘tdingiz!\nID: <b>{public_id}</b>",
        parse_mode='HTML',
        reply_markup=main_menu()
    )

# --- TASKS ---
@bot.message_handler(func=lambda m: m.text == "Bugungi vazifalar ✅")
def show_tasks(message):
    user = get_user(message.chat.id)

    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for task in DAILY_TASKS:
        markup.add(KeyboardButton(task))
    markup.add(KeyboardButton("Orqaga ⬅️"))

    bot.send_message(message.chat.id,
        f"{user['daily_count']}/{len(DAILY_TASKS)} bajarildi",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: m.text in DAILY_TASKS)
def complete_task(message):
    user = get_user(message.chat.id)

    if message.text in user['completed_tasks']:
        bot.send_message(message.chat.id, "⚠️ Allaqachon bajarilgan")
        return

    user['completed_tasks'].append(message.text)
    user['daily_count'] += 1
    user['total_score'] += 10

    bot.send_message(message.chat.id, "✅ +10 ball")
    bot.send_message(message.chat.id, random.choice(MOTIVATIONS))

# --- FINISH ---
@bot.message_handler(func=lambda m: m.text == "Finish 🏁")
def finish_day(message):
    user = get_user(message.chat.id)

    if user['daily_count'] == 0:
        bot.send_message(message.chat.id, "Hech narsa qilinmadi 😅")
        return

    percent = int((user['daily_count'] / len(DAILY_TASKS)) * 100)

    user['history'].append(f"{datetime.now().strftime('%d/%m')} - {percent}%")

    if percent == 100:
        bot.send_message(message.chat.id, "🔥 PERFECT!")
        bot.send_animation(message.chat.id, random.choice(GIFS))

    user['daily_count'] = 0
    user['completed_tasks'] = []

    bot.send_message(message.chat.id,
        f"Natija: {percent}%",
        reply_markup=main_menu()
    )

# --- RANK ---
@bot.message_handler(func=lambda m: m.text == "Reyting 📊")
def show_ranking(message):
    sorted_users = sorted(user_data.items(), key=lambda x: x[1]['total_score'], reverse=True)

    text = "🏆 <b>REYTING</b>\n\n"
    for i, (uid, data) in enumerate(sorted_users):
        text += f"{i+1}. {data['info'].get('public_id')} — {data['total_score']} ball\n"

    bot.send_message(message.chat.id, text, parse_mode='HTML')

# --- RESULTS ---
@bot.message_handler(func=lambda m: m.text == "Natijalar jadvali 🏆")
def show_results(message):
    user = get_user(message.chat.id)

    history = "\n".join(user['history']) if user['history'] else "Bo'sh"

    bot.send_message(message.chat.id, f"📊 Natijalar:\n{history}")

# --- BACK ---
@bot.message_handler(func=lambda m: m.text == "Orqaga ⬅️")
def back(message):
    bot.send_message(message.chat.id, "Menu:", reply_markup=main_menu())

# --- REMINDER SYSTEM ---
def reminder_loop():
    while True:
        now = datetime.now().hour

        for uid in user_data:
            try:
                if 9 <= now < 12:
                    bot.send_message(uid, random.choice(REMINDERS["morning"]))
                elif 15 <= now < 17:
                    bot.send_message(uid, random.choice(REMINDERS["afternoon"]))
                elif 18 <= now < 22:
                    bot.send_message(uid, random.choice(REMINDERS["evening"]))
            except:
                pass

        time.sleep(3600)

threading.Thread(target=reminder_loop, daemon=True).start()

# --- RUN ---
bot.infinity_polling()
