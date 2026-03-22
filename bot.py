import telebot
import os
import random
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Railway Variables'dan ma'lumotlarni olish
TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "6338204692")) # Sizning ID raqamingiz
bot = telebot.TeleBot(TOKEN)

# Vazifalar ro'yxati (Yangi sarmoya vazifasi qo'shildi)
TASKS = {
    "detox": "Tongda detox (1 soat) 📵",
    "book": "Kitob mutolasi 📚",
    "sugar": "Sugar detox 🍬",
    "drink": "Gazsiz ichimliklar 🥤",
    "invest": "5000 so'm sarmoya 💰"
}

# Hissiyotni "qitiqlaydigan" motivatsiyalar
MOTIVATIONS = [
    " 'Ertaga' — bu dangasalarning qabristoni. Bugun qilmasangiz, u yerga orzularingizni ko'masiz.",
    "Siz 'vaqtim bor' deb o'ylaysiz. Eng katta xatoyingiz ham shunda.",
    "Hozir uxlayotganingizda, kimdir siz istagan cho'qqini zabt etyapti.",
    "Ter to'kishni istamasangiz, ko'z yoshi to'kishga tayyor turing.",
    "Uyquingiz orzularingizdan shirinroq bo'lsa, uyg'onishingizdan ma'no yo'q.",
    "Bugun o'zingizga qiyin qilsangiz, ertaga hayot sizga oson bo'ladi.",
    "Siz boshqalarning nusxasi bo'lish uchun tug'ilmagansiz!"
]

# Foydalanuvchi ma'lumotlarini saqlash (Vaqtinchalik lug'at)
user_data = {}

def get_main_keyboard():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(KeyboardButton("Bugungi vazifalar ✅"))
    markup.add(KeyboardButton("Natijalar jadvali 🏆")) # Leaderboard o'rniga
    markup.add(KeyboardButton("Finish 🏁"))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    user_data[user_id] = {task: False for task in TASKS}
    
    welcome_msg = (
        "Assalomu alaykum! 21 kunlik challenge'ga xush kelibsiz! 🔥\n\n"
        "Har kuni vazifalarni bajaring va o'z ustingizda ishlang.\n"
        "<i>Bu bot MBE Useful tomonidan yaratilgan.</i>" # Mualliflik yozuvi
    )
    bot.send_message(message.chat.id, welcome_msg, reply_markup=get_main_keyboard(), parse_mode='HTML')

@bot.message_handler(func=lambda message: message.text == "Bugungi vazifalar ✅")
def show_tasks(message):
    user_id = message.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {task: False for task in TASKS}
    
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for key, task_name in TASKS.items():
        status = "✅" if user_data[user_id][key] else "❌"
        markup.add(KeyboardButton(f"{task_name} {status}"))
    markup.add(KeyboardButton("Asosiy menyu 🔙"))
    
    # Har safar vazifalarni ochganda bitta motivatsiya yuboradi
    motivation = random.choice(MOTIVATIONS)
    bot.send_message(message.chat.id, f"💡 {motivation}\n\nVazifalarni bajaring:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Finish 🏁")
def finish_day(message):
    user_id = message.from_user.id
    if user_id not in user_data:
        bot.send_message(message.chat.id, "Avval vazifalarni boshlang!")
        return

    # Foiz hisoblash
    done_count = sum(1 for status in user_data[user_id].values() if status)
    total_count = len(TASKS)
    percent = int((done_count / total_count) * 100)
    
    response = (
        f"🏁 1-kun muvaffaqiyatli bajarildi: {percent}%\n\n"
        "<b>Siz dunyodagi eng yaxshi insonsiz! E vapshe gap yo'q!</b> 🔥\n\n"
        "Ertaga yanada kuchliroq bo'lamiz!"
    )
    bot.send_message(message.chat.id, response, parse_mode='HTML', reply_markup=get_main_keyboard())

# Vazifani bajarilgan deb belgilash logicasi (qisqacha)
@bot.message_handler(func=lambda message: any(task in message.text for task in TASKS.values()))
def complete_task(message):
    user_id = message.from_user.id
    for key, val in TASKS.items():
        if val in message.text:
            user_data[user_id][key] = True
            bot.send_message(message.chat.id, f"Barakalla! '{val}' bajarildi! 🎉")
            show_tasks(message)
            break

@bot.message_handler(func=lambda message: message.text == "Asosiy menyu 🔙")
def back_home(message):
    bot.send_message(message.chat.id, "Asosiy menyu:", reply_markup=get_main_keyboard())

@bot.message_handler(func=lambda message: message.text == "Natijalar jadvali 🏆")
def show_results(message):
    bot.send_message(message.chat.id, "🏆 Hozircha siz 1-o'rindasiz! (Jadval tez orada yangilanadi)")

bot.infinity_polling()
