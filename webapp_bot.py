import telebot
import os
import random
import json
from datetime import datetime
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

# 1. BOTNI ANIQLASH (TOKENNI OLISH)
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# 2. MA'LUMOTLARNI SAQLASH VA YUKLASH
user_data = {}

def load_data():
    global user_data
    if os.path.exists('users_db.json'):
        with open('users_db.json', 'r') as f:
            user_data = json.load(f)

def save_data():
    with open('users_db.json', 'w') as f:
        json.dump(user_data, f)

def get_user(chat_id):
    chat_id = str(chat_id)
    if chat_id not in user_data:
        user_data[chat_id] = {'total_score': 0, 'history': []}
    return user_data[chat_id]

load_data()

# 3. MINI APP-DAN MA'LUMOT QABUL QILISH (MOTIVATSIYA)
@bot.message_handler(content_types=['web_app_data'])
def web_app_receive(message):
    data = json.loads(message.web_app_data.data)
    
    if data.get('action') == "task_done":
        user = get_user(message.chat.id)
        task = data.get('task')
        
        user['total_score'] += 10
        save_data()
        
        mots = [
            f"🔥 Dahshat! {task} bajarildi. Davom et!",
            f"💪 Intizom — bu o'ziga berilgan va'dani bajarishdir. +10 ball!",
            f"🌟 Siz bugun kechagidan yaxshiroqsiz!"
        ]
        bot.send_message(message.chat.id, random.choice(mots))

# 4. KOMANDALAR VA START
@bot.message_handler(commands=['start'])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    # Shaxsiy kabinet tugmasi (Web App linkini o'zingizniki bilan almashtiring)
    web_app_url = "https://muminbaevshohjahon-bit.github.io/telegram-bot/" 
    btn_kabinet = KeyboardButton("Shaxsiy Kabinet 📱", web_app=WebAppInfo(url=web_app_url))
    btn_finish = KeyboardButton("Finish 🏁")
    markup.add(btn_kabinet)
    markup.add(btn_finish)
    
    bot.send_message(message.chat.id, "Xush kelibsiz! Vazifalarni bajarishni boshlaymiz.", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "Finish 🏁")
def finish_day(message):
    user = get_user(message.chat.id)
    last_date = datetime.now().strftime('%d/%m')
    
    if any(last_date in entry for entry in user['history']):
        bot.send_message(message.chat.id, "Bugun uchun allaqachon yakunlagansiz. ✨")
        return
    
    user['history'].append(f"{last_date} - Yakunlandi")
    save_data()
    bot.send_message(message.chat.id, "Kun yakunlandi! Natijalaringiz saqlandi. 🏁")

# 5. BOTNI ISHGA TUSHIRISH
if __name__ == "__main__":
    print("Bot ishga tushdi...")
    bot.polling(none_stop=True)
