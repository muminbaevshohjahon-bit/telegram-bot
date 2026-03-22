from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

def main_menu():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    
    # MUHIM: O'zingizning GitHub Pages linkigizni qo'ying
    web_link = "https://muminbaevshohjahon-bit.github.io/telegram-bot/"
    
    btn_webapp = KeyboardButton("Shaxsiy Kabinet 📊", web_app=WebAppInfo(url=web_link))
    btn_tasks = KeyboardButton("Bugungi vazifalar ✅")
    btn_results = KeyboardButton("Natijalar jadvali 🏆")
    btn_rank = KeyboardButton("Reyting 📈")
    btn_finish = KeyboardButton("Finish 🏁")
    
    markup.add(btn_webapp) 
    markup.add(btn_tasks, btn_results)
    markup.add(btn_rank, btn_finish)
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    uid = str(message.chat.id)
    user = get_user(uid)
    
    # Agar foydalanuvchi ismi bazada bo'lsa, ro'yxatdan o'tkazma, menyuni ko'rsat
    if user.get('info', {}).get('name'):
        user['step'] = 'main'
        bot.send_message(uid, f"Xush kelibsiz, {user['info']['name']}!", reply_markup=main_menu())
    else:
        user['step'] = 'get_name'
        bot.send_message(uid, "<b>Assalomu alaykum!</b>\nIsmingizni kiriting:", parse_mode='HTML')
    save_data()
