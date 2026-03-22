import telebot
import os
import random
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime

TOKEN = os.getenv("TOKEN") or "YOUR_BOT_TOKEN"
bot = telebot.TeleBot(TOKEN)

# Ma'lumotlar bazasi (Xotira)
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
    "Mukammallikni kutma — harakatni boshlash muhim.",
    "Sen o‘ylagandan ham kuchlisan.",
    "Qiyinchilik — bu yashirin imkoniyat.",
    "Har kuni kichik qadam — katta natija.",
    "Sen taslim bo‘lmaguningcha, yutqazmading.",
    "Eng yaxshi vaqt — hozir.",
    "Harakat — motivatsiyadan muhimroq."
]

GIFS = [
    "https://media.giphy.com/media/3o7TKDkDbIDJieKbVm/giphy.gif",
    "https://media.giphy.com/media/FACfMgP1N9mlG/giphy.gif",
    "https://media.giphy.com/media/XMnjfm65r82TirNhoe/giphy.gif",
    "https://media.giphy.com/media/x4dS8uOkeEFdxvV1nz/giphy.gif",
]

# --- YORDAMCHI FUNKSIYALAR ---

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

# --- RO'YXATDAN O'TISH ---

@bot.message_handler(commands=['start'])
def start(message):
    uid = message.chat.id
    user = get_user(uid)

    user['step'] = 'get_name'
    bot.send_message(uid,
        "<b>Assalomu alaykum!</b>\n30-kunlik challenge botiga xush kelibsiz!\n\nIsmingizni kiriting:",
        parse_mode='HTML'
    )

@bot.message_handler(func=lambda m: get_user(m.chat.id)['step'] == 'get_name')
def get_name(message):
    user = get_user(message.chat.id)
    user['info']['name'] = message.text
    user['step'] = 'get_birth'

    bot.send_message(message.chat.id,
        "Tug'ilgan yilingizni kiriting (masalan: 2003):"
    )

@bot.message_handler(func=lambda m: get_user(m.chat.id)['step'] == 'get_birth')
def get_birth(message):
    uid = message.chat.id
    user = get_user(uid)

    if not message.text.isdigit():
        bot.send_message(uid, "❗ Iltimos faqat yil kiriting!")
        return

    user['info']['birth_year'] = message.text
    user['step'] = 'get_nick'

    bot.send_message(uid, "Nickname tanlang:")

@bot.message_handler(func=lambda m: get_user(m.chat.id)['step'] == 'get_nick')
def get_nick(message):
    uid = message.chat.id
    user = get_user(uid)

    user['info']['nickname'] = message.text
    user['step'] = 'main'

    reg_id = f"MBE-{random.randint(1000,9999)}"
    user['info']['reg_id'] = reg_id

    bot.send_message(uid,
        f"Rahmat, {user['info']['name']}!\nID: {reg_id}",
        reply_markup=main_menu()
    )

# --- ASOSIY FUNKSIYALAR ---

@bot.message_handler(func=lambda m: m.text == "Bugungi vazifalar ✅")
def show_tasks(message):
    user = get_user(message.chat.id)

    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for task in DAILY_TASKS:
        markup.add(KeyboardButton(task))

    markup.add(KeyboardButton("Orqaga ⬅️"))

    bot.send_message(message.chat.id,
        f"📊 {user['daily_count']}/{len(DAILY_TASKS)}",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: m.text in DAILY_TASKS)
def complete_task(message):
    uid = message.chat.id
    user = get_user(uid)

    if message.text in user['completed_tasks']:
        bot.send_message(uid, "⚠️ Bu vazifa allaqachon bajarilgan")
        return

    user['completed_tasks'].append(message.text)
    user['daily_count'] += 1
    user['total_score'] += 10

    bot.send_message(uid, "✅ Bajarildi! +10 ball")
    bot.send_message(uid, random.choice(MOTIVATIONS))
    bot.send_animation(uid, random.choice(GIFS))

@bot.message_handler(func=lambda m: m.text == "Finish 🏁")
def finish_day(message):
    uid = message.chat.id
    user = get_user(uid)

    if user['daily_count'] == 0:
        bot.send_message(uid, "Hech narsa bajarmadingiz 😅")
        return

    percent = int((user['daily_count'] / len(DAILY_TASKS)) * 100)

    user['history'].append(
        f"{datetime.now().strftime('%d/%m')} - {percent}%"
    )

    user['daily_count'] = 0
    user['completed_tasks'] = []

    bot.send_message(uid,
        f"🏁 Natija: {percent}%",
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda m: m.text == "Reyting 📊")
def show_ranking(message):
    sorted_users = sorted(
        user_data.items(),
        key=lambda x: x[1]['total_score'],
        reverse=True
    )

    text = "🏆 <b>REYTING</b>\n\n"
    for i, (uid, data) in enumerate(sorted_users):
        text += f"{i+1}. {data['info'].get('nickname','User')} — {data['total_score']} ball\n"

    bot.send_message(message.chat.id, text, parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "Natijalar jadvali 🏆")
def show_results(message):
    user = get_user(message.chat.id)

    history = "\n".join(user['history']) if user['history'] else "Bo'sh"

    bot.send_message(message.chat.id,
        f"📊 Natijalar:\n{history}"
    )

@bot.message_handler(func=lambda m: m.text == "Orqaga ⬅️")
def back(message):
    bot.send_message(message.chat.id, "Menu:", reply_markup=main_menu())

bot.infinity_polling()
