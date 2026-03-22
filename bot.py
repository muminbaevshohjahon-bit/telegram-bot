import telebot
import os
import random
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from apscheduler.schedulers.background import BackgroundScheduler

# Railway Variables
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# Ma'lumotlarni saqlash (Oddiy lug'at ko'rinishida, lekin haqiqiy loyihada DB ishlatish tavsiya etiladi)
user_data = {} 

# Vazifalar ro'yxati
DAILY_TASKS = [
    "Tongda detox (1 soat) 📵",
    "Kitob mutolasi 📚",
    "Sugar detox 🍬",
    "Gazsiz ichimliklar 🥤",
    "5000 so'm sarmoya 💰",
    "Jismoniy mashq 💪",
    "1 daqiqa hech narsa qilmaslik 🧘‍♂️"
]

# Motivatsiyalar va Tabriklar
MOTIVATIONS = ["Sen boshlamasang, hech narsa boshlanmaydi.", "Bugungi og‘riq — ertangi kuch.", "Eng katta raqibing — kechagi o‘zing."]
CONGRATS = ["Biz kutgandik, bilgandik shunday bo'lishini! 🌟", "Porloq kelajak seni qo'lingda! ✨", "Sen bilan faxrlanaman! ✊"]
GIFS = [
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExeTVrZWJ3cWU2MDgzbTV3NGk5NWtocnNwdGJvd2cxMnJwMTRtN2RhYSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/3oEduUGL2JaSK7oS76/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3eW1hbnAyazN6OTRqa2R5ZHYyb250eHI4aW5zODFzZm0zOGFpOGt0NyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/ahDOY7XwxjNXW/giphy.gif"
]

# --- YORDAMCHI FUNKSIYALAR ---

def get_user_stats(uid):
    if uid not in user_data:
        user_data[uid] = {'daily_count': 0, 'history': [], 'total_days': 0}
    return user_data[uid]

def main_menu():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add(KeyboardButton("Bugungi vazifalar ✅"), KeyboardButton("Natijalar jadvali 🏆"), KeyboardButton("Finish 🏁"))
    return markup

# --- HANDLERLAR ---

@bot.message_handler(commands=['start'])
def start(message):
    uid = message.chat.id
    get_user_stats(uid)
    bot.send_message(uid, "<b>30 kunlik challenge'ga xush kelibsiz!</b> 🔥", parse_mode='HTML', reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == "Bugungi vazifalar ✅")
def show_tasks(message):
    uid = message.chat.id
    stats = get_user_stats(uid)
    motivation = random.choice(MOTIVATIONS)
    
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for task in DAILY_TASKS:
        markup.add(KeyboardButton(task))
    markup.add(KeyboardButton("Orqaga ⬅️"))
    
    bot.send_message(uid, f"💡 **Motivatsiya:**\n'{motivation}'\n\nBugun bajarildi: {stats['daily_count']}/{len(DAILY_TASKS)}\n👇 Tanlang:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in DAILY_TASKS)
def complete_task(message):
    uid = message.chat.id
    stats = get_user_stats(uid)
    stats['daily_count'] += 1
    
    txt = random.choice(CONGRATS)
    gif = random.choice(GIFS)
    bot.send_animation(uid, gif, caption=f"✨ {txt}\n\nBugungi natijangiz: {stats['daily_count']}/{len(DAILY_TASKS)}")

@bot.message_handler(func=lambda m: m.text == "Finish 🏁")
def finish_day(message):
    uid = message.chat.id
    stats = get_user_stats(uid)
    
    if stats['daily_count'] > 0:
        stats['total_days'] += 1
        stats['history'].append(f"{stats['total_days']}-kun: {stats['daily_count']} ta vazifa")
        res = stats['daily_count']
        stats['daily_count'] = 0 # Ertangi kun uchun nolga tushirish
        
        bot.send_message(uid, f"🏁 **Kun yakunlandi!**\nBugun {res} ta vazifa bajardingiz. Sen bilan faxrlanaman! ✊", reply_markup=main_menu())
    else:
        bot.send_message(uid, "Bugun hali borta ham vazifa bajarmadingiz-ku? 🤨", reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == "Natijalar jadvali 🏆")
def show_leaderboard(message):
    uid = message.chat.id
    stats = get_user_stats(uid)
    
    if not stats['history']:
        msg = "Hozircha natijalar yo'q. Bugun birinchi kunni yakunlang! 🚀"
    else:
        msg = "🏆 **Sizning 30 kunlik natijalaringiz:**\n\n" + "\n".join(stats['history'])
    
    bot.send_message(uid, msg, reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == "Orqaga ⬅️")
def back
