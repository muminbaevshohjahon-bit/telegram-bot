import telebot
import os
import random
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# Ma'lumotlar bazasi (Xotira)
user_data = {}

DAILY_TASKS = [
    "Tongda detox (1 soat) 📵", "Kitob mutolasi 📚", "Sugar detox 🍬",
    "Gazsiz ichimliklar 🥤", "5000 so'm sarmoya 💰", "Jismoniy mashq 💪",
    "1 daqiqa hech narsa qilmaslik 🧘‍♂️"
]

MOTIVATIONS = ["G'alaba intizomni sevadi.", "Bugungi mehnat — ertangi faxr.", "O'zingni yeng!"]
GIFS = ["https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3eXJqM3Z4eXp5bmZ6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6JmR6PTEmZ3R6Z3R6/3o7TKDkDbIDJieKbVm/giphy.gif"]

# --- YORDAMCHI FUNKSIYALAR ---

def get_user(uid):
    if uid not in user_data:
        user_data[uid] = {
            'info': {}, 
            'daily_count': 0, 
            'history': [], 
            'total_score': 0, # Reyting uchun umumiy ball
            'step': 'start'
        }
    return user_data[uid]

def main_menu():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add(KeyboardButton("Bugungi vazifalar ✅"), KeyboardButton("Natijalar jadvali 🏆"), KeyboardButton("Reyting 📊"), KeyboardButton("Finish 🏁"))
    return markup

# --- RO'YXATDAN O'TISH QISMI ---

@bot.message_handler(commands=['start'])
def start(message):
    uid = message.chat.id
    user = get_user(uid)
    
    welcome_text = (
        "<b>Assalomu aleykum!</b>\n"
        "30-kunlik chellenj botiga xush kelibsiz!\n\n"
        "<i>Bot MBE useful tomonidan yaratilgan.</i>\n\n"
        "Keling, tanishib olaylik! <b>Ismingizni kiriting:</b>"
    )
    user['step'] = 'get_name'
    bot.send_message(uid, welcome_text, parse_mode='HTML')

@bot.message_handler(func=lambda m: get_user(m.chat.id)['step'] == 'get_name')
def get_name(message):
    uid = message.chat.id
    user = get_user(uid)
    user['info']['name'] = message.text
    user['step'] = 'get_birth'
    bot.send_message(uid, "<b>Tug'ilgan yilingizni kiriting (masalan: 2003):</b>", parse_mode='HTML')

@bot.message_handler(func=lambda m: get_user(m.chat.id)['step'] == 'get_birth')
def get_birth(message):
    uid = message.chat.id
    user = get_user(uid)
    user['info']['birth_year'] = message.text
    user['step'] = 'get_nick'
    bot.send_message(uid, "<b>O'zingizga nickname tanlang :)</b>", parse_mode='HTML')

@bot.message_handler(func=lambda m: get_user(m.chat.id)['step'] == 'get_nick')
def get_nick(message):
    uid = message.chat.id
    user = get_user(uid)
    user['info']['nickname'] = message.text
    user['step'] = 'main'
    
    reg_id = f"MBE-{random.randint(1000, 9999)}"
    user['info']['reg_id'] = reg_id
    
    success_msg = (
        f"Rahmat! Tanishganimdan xursandman, {user['info']['name']}!\n"
        f"Sizning ID raqamingiz: <b>{reg_id}</b>\n\n"
        "Endi boshlashga tayyorman! Quyidagi menyudan vazifalarni tanlang."
    )
    bot.send_message(uid, success_msg, parse_mode='HTML', reply_markup=main_menu())

# --- ASOSIY FUNKSIYALAR ---

@bot.message_handler(func=lambda m: m.text == "Bugungi vazifalar ✅")
def show_tasks(message):
    uid = message.chat.id
    stats = get_user(uid)
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for task in DAILY_TASKS:
        markup.add(KeyboardButton(task))
    markup.add(KeyboardButton("Orqaga ⬅️"))
    bot.send_message(uid, f"📊 Bugun: {stats['daily_count']}/{len(DAILY_TASKS)}\nID: {stats['info'].get('reg_id')}", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in DAILY_TASKS)
def complete_task(message):
    uid = message.chat.id
    stats = get_user(uid)
    stats['daily_count'] += 1
    stats['total_score'] += 10 # Har bir vazifa uchun 10 ball
    bot.send_message(uid, f"✅ Bajarildi! Ball: +10")

@bot.message_handler(func=lambda m: m.text == "Finish 🏁")
def finish_day(message):
    uid = message.chat.id
    stats = get_user(uid)
    if stats['daily_count'] == 0:
        bot.send_message(uid, "Hali birorta ham vazifa bajarmadingiz-ku? 🤨")
        return

    percent = int((stats['daily_count'] / len(DAILY_TASKS)) * 100)
    stats['history'].append(f"{datetime.now().strftime('%d/%m')}: {percent}%")
    stats['daily_count'] = 0 
    
    bot.send_message(uid, f"🏁 Kun yakunlandi! Bugungi natija: {percent}%\nSiz reytingda ko'tarilmoqdasiz!", reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == "Reyting 📊")
def show_ranking(message):
    # Reytingni ballar bo'yicha saralash
    sorted_users = sorted(user_data.items(), key=lambda x: x[1]['total_score'], reverse=True)
    
    ranking_text = "🏆 **UMUMIY REYTING**\n\n"
    user_pos = 0
    
    for i, (uid, data) in enumerate(sorted_users):
        nick = data['info'].get('nickname', 'User')
        score = data['total_score']
        ranking_text += f"{i+1}. {nick} — {score} ball\n"
        if uid == message.chat.id:
            user_pos = i + 1
            
    ranking_text += f"\n👤 Sizning o'rningiz: {user_pos}-o'rin"
    bot.send_message(message.chat.id, ranking_text, parse_mode='Markdown')

@bot.message_handler(func=lambda m: m.text == "Natijalar jadvali 🏆")
def show_results(message):
    uid = message.chat.id
    user = get_user(uid)
    history = "\n".join(user['history']) if user['history'] else "Hozircha bo'sh"
    bot.send_message(uid, f"🚀 **{user['info'].get('nickname')}** natijalari:\n\n{history}", parse_mode='Markdown')

@bot.message_handler(func=lambda m: m.text == "Orqaga ⬅️")
def back(message):
    bot.send_message(message.chat.id, "Asosiy menyu:", reply_markup=main_menu())

bot.infinity_polling()
