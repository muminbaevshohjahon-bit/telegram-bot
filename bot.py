import telebot
import os
import random
import json
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# Ma'lumotlarni faylga saqlash
def save_data():
    try:
        with open('users_db.json', 'w') as f:
            json.dump(user_data, f)
    except Exception as e:
        print(f"Saqlashda xato: {e}")

def load_data():
    if os.path.exists('users_db.json'):
        try:
            with open('users_db.json', 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

user_data = load_data()

DAILY_TASKS = [
    "Tongda detox (1 soat) 📵", "Kitob mutolasi 📚", "Sugar detox 🍬",
    "Gazsiz ichimliklar 🥤", "5000 so'm sarmoya 💰", "Jismoniy mashq 💪",
    "1 daqiqa hech narsa qilmaslik 🧘‍♂️"
]

MOTIVATIONS = ["G'alaba intizomni sevadi.", "Bugungi mehnat — ertangi faxr.", "O'zingni yeng!"]
GIFS = ["https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3eXJqM3Z4eXp5bmZ6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6JmR6PTEmZ3R6Z3R6/3o7TKDkDbIDJieKbVm/giphy.gif"]

def get_user(uid
