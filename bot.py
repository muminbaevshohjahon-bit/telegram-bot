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

MOTIVATIONS = [
    "Sen boshlamasang, hech narsa boshlanmaydi.", "Bugungi og‘riq — ertangi kuch.",
    "Sen o‘ylagandan ham kuchlisan.", "Eng katta raqibing — kechagi o‘zing.",
    "Harakat — motivatsiyadan muhimroq.", "Vaqt ketmoqda — senchi?",
    "Intizom — erkinlik kaliti.", "Eng zo‘r vaqt — hozir."
]

GIFS = [
    "https://media.giphy.com/media/3o7TKDkDbIDJieKbVm/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3eGE4bTFqbXo1eTFub2FhODBqNmgyZ3ZoNWZreWR6cDd1bDFicGxsNSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/vBbGN3xEJZfiWHiGW9/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaXU3bGl0dXg3c3FxM3VuZnl1ZW8wamRlbW5vbncxN2V1enNoNjhxOCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/g9582DNuQppxC/giphy.gif",
    "https://media.giphy.com/media/FACfMgP1N9mlG/giphy.gif"
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

# --- REGISTRATION (TUZATILDI) ---
@bot.message_handler(commands=['start'])
def start(message):
    uid = str(message.chat.id)
    user = get_user(uid)
    
    welcome_text = (
        "<b><i>Assalomu aleykum hush kelibsiz!</i></b>\n"
        "<b><i>Men MBE useful tomonidan yaratilgan botman!</i></b>\n\n"
        "<b><i>Maqsadimiz 30 kunlik chellenj davomida intizomni shakllantirish.</i></b>\n"
        "<b><i>Balki foydasi tegar...</i></b>\n\n"
        "Keling tanishib olaylik... Ismingizni kiriting:"
    )
    
    user['step'] = 'get_name'
    save_data()
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
    bot.send_message(message.chat.id, f"Tabrikleyshn ro‘yxatdan o‘tdingiz! 🔥 ID: <b>{public_id}</b>", parse_mode='HTML', reply_markup=main_menu())

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

@bot.message_handler(func=lambda m: m.text == "Finish 🏁")
def finish_day(message):
    user = get_user(message.chat.id)
    if user['daily_count'] == 0:
        bot.send_message(message.chat.id, "Hech bo'lmasa bitta vazifa bajaring!")
        return
    percent = int((user['daily_count'] / len(DAILY_TASKS)) * 100)
    user['history'].append(f"{datetime.now().strftime('%d/%m')} - {percent}%")
    motivation = random.choice(MOTIVATIONS)
    gif = random.choice(GIFS)
    bot.send_animation(message.chat.id, gif, caption=f"🏁 <b>Kun yakunlandi!✊</b>\nNatija: {percent}%\n\n<i>{motivation}</i>", parse_mode='HTML')
    user['daily_count'] = 0
    user['completed_tasks'] = []
    save_data()

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

def reminder_loop():
    while True:
        now = datetime.now().hour
        if 9 <= now <= 22:
            for uid in list(user_data.keys()):
                try:
                    if user_data[uid].get('step') == 'main':
                        bot.send_message(uid, f"💡 <b>Motivatsiya:</b>\n\n{random.choice(MOTIVATIONS)}", parse_mode='HTML')
                except: pass
        time.sleep(3600)

threading.Thread(target=reminder_loop, daemon=True).start()

# --- RUN (Conflict xatosini oldini olish uchun) ---
if __name__ == "__main__":
    bot.infinity_polling(skip_pending=True)
