import telebot
import os
import random
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from apscheduler.schedulers.background import BackgroundScheduler

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# Ma'lumotlarni saqlash
user_data = {}

# 100 ta Motivatsiya (Qisqartirilgan, hammasini joylang)
MOTIVATIONS = [
    "Sen boshlamasang, hech narsa boshlanmaydi.", "Mukammallikni kutma — harakatni boshlash muhim.",
    "Bugungi og‘riq — ertangi kuch.", "Sen o‘ylagandan ham kuchlisan.",
    "Hech kim seni qutqarmaydi — o‘zingni o‘zing ko‘tar.", "Qiyinchilik — bu yashirin imkoniyat.",
    "Orzular faqat harakat bilan haqiqatga aylanadi.", "Qo‘rqish — o‘sish boshlanishidir.",
    "Har kuni kichik qadam — katta natija.", "Sen taslim bo‘lmaguningcha, yutqazmading.",
    # ... qolgan 90 tasi ham shu ro'yxatda bo'lsin
    "Boshlagin. Hozir. Shu yerda."
]

GIFS = [
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExeTVrZWJ3cWU2MDgzbTV3NGk5NWtocnNwdGJvd2cxMnJwMTRtN2RhYSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/3oEduUGL2JaSK7oS76/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3eW1hbnAyazN6OTRqa2R5ZHYyb250eHI4aW5zODFzZm0zOGFpOGt0NyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/ahDOY7XwxjNXW/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOTVkZ3hueXBnNjkwZ2J1YjJkN2gwMHN3b3M3aXZ0cnRvMDFpbHdkZyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/FACfMgP1N9mlG/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3ZTc5MnQxOTdhY3dnMWpuNXFmdzJ0dnR1Z29hMGV4cnVnaXp1YmtqbiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/IHETYBuNarfOwyDBrY/giphy.gif"
]

CONGRATS = ["Biz kutgandik!", "Porloq kelajak seni qo'lingda!", "Sen bilan faxrlanaman!", "Malades!"]

# Ro'yxatdan o'tish bosqichlari
@bot.message_handler(commands=['start'])
def start_reg(message):
    bot.send_message(message.chat.id, "Assalomu alaykum! Ro'yxatdan o'tishni boshlaymiz. Ismingiz nima?")
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    user_data[message.chat.id] = {'name': message.text}
    bot.send_message(message.chat.id, "Tug'ilgan yilingizni kiriting (masalan: 2004):")
    bot.register_next_step_handler(message, get_year)

def get_year(message):
    user_data[message.chat.id]['year'] = message.text
    bot.send_message(message.chat.id, "Nickname-ingizni kiriting:")
    bot.register_next_step_handler(message, finish_reg)

def finish_reg(message):
    user_data[message.chat.id]['nick'] = message.text
    name = user_data[message.chat.id]['name']
    
    welcome_msg = (
        f"Assalomu alaykum {name}! <b>30 kunlik challenge'ga xush kelibsiz!</b> 🔥\n\n"
        "Har kuni vazifalarni bajaring va o'z ustingizda ishlang.\n"
        "Bu bot <b>MBE Useful</b> tomonidan yaratilgan. Foydasi tegsa xursandmiz!"
    )
    
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(KeyboardButton("Bugungi vazifalar ✅"), KeyboardButton("Natijalar jadvali 🏆"), KeyboardButton("Finish 🏁"))
    
    bot.send_message(message.chat.id, welcome_text, parse_mode='HTML', reply_markup=markup)

# Vazifa bajarilganda
@bot.message_handler(func=lambda m: "✅" in m.text)
def handle_done(message):
    congrat = random.choice(CONGRATS)
    gif = random.choice(GIFS)
    bot.send_animation(message.chat.id, gif, caption=congrat)

bot.infinity_polling()
