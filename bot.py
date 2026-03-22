import telebot
import os
import random
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from apscheduler.schedulers.background import BackgroundScheduler

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# Ma'lumotlarni saqlash
user_data = {} 

DAILY_TASKS = [
    "Tongda detox (1 soat) 📵", "Kitob mutolasi 📚", "Sugar detox 🍬",
    "Gazsiz ichimliklar 🥤", "5000 so'm sarmoya 💰", "Jismoniy mashq 💪",
    "1 daqiqa hech narsa qilmaslik 🧘‍♂️"
]

# 100 TA MOTIVATSIYA RO'YXATI
MOTIVATIONS = [
    "Sen boshlamasang, hech narsa boshlanmaydi.", "Bugungi og‘riq — ertangi kuch.", "Eng katta raqibing — kechagi o‘zing.",
    "Mukammallikni kutma — harakatni boshlash muhim.", "Sen o‘ylagandan ham kuchlisan.", "Qiyinchilik — bu yashirin imkoniyat.",
    "Orzular faqat harakat bilan haqiqatga aylanadi.", "Qo‘rqish — o‘sish boshlanishidir.", "Har kuni kichik qadam — katta natija.",
    "Sen taslim bo‘lmaguningcha, yutqazmading.", "Bahonalar seni orqaga tortadi.", "Harakat — motivatsiyadan muhimroq.",
    "Vaqt ketmoqda — senchi?", "Sen bunga loyiqsan — lekin ishlashing kerak.", "Og‘ir bo‘lsa ham davom et.",
    "O‘zgarish og‘riqli, lekin zarur.", "Qanchalik qiynalsang, shunchalik kuchli bo‘lasan.", "Natija sabrni yaxshi ko‘radi.",
    "Bugun qilmaganing — ertaga pushaymon bo‘ladi.", "Sen o‘zingning hayoting uchun javobgarsan.", "Kichik boshlashdan uyalmagin.",
    "Har kuni o‘zingni yeng.", "Kuch — ichingda. Uni uyg‘ot.", "Taslim bo‘lish — eng oson yo‘l.",
    "Eng yaxshi vaqt — hozir.", "Qancha ko‘p harakat, shuncha kam pushaymon.", "Qiyinchilik seni sinaydi, sindirmaydi.",
    "Yutuq — intizom natijasi.", "Orzularing seni kutmaydi.", "Qo‘rquv ortida — erkinlik bor.",
    "Hech kim senga majbur emas — o‘zingni isbotla.", "Harakat qil, hatto mukammal bo‘lmasa ham.", "Yiqildingmi? Tur va davom et.",
    "Sen hali boshlamading ham.", "Qanchalik ko‘p urinma, shunchalik yaqinlashasan.", "Og‘riq vaqtinchalik — natija abadiy.",
    "Bugungi mehnat — ertangi faxr.", "Sen o‘zingni o‘zgartirsang, hayoting o‘zgaradi.", "Kuchli bo‘lish — tanlov.",
    "Intizom — erkinlik kaliti.", "Qachon qiyin bo‘lsa — o‘sha payt o‘sasan.", "Orqaga emas, oldinga qaragin.",
    "O‘z ustingda ishlash — eng yaxshi investitsiya.", "Sen bunga qodirsan.", "Kech emas — hali vaqt bor.",
    "Boshlash — yarim g‘alaba.", "Kuchli odamlar bahona qilmaydi.", "Har kuni yangi imkoniyat.",
    "Sen taslim bo‘lsang — hammasi tugaydi.", "Sen davom etsang — hammasi boshlanadi.", "O‘z yo‘lingni o‘zing yarat.",
    "Orzularing seni chaqiryapti.", "Qadam tashla — yo‘l ochiladi.", "O‘zinga ishongan odam yutadi.",
    "Harakat qil, hatto sekin bo‘lsa ham.", "Katta natija — kichik odatlardan boshlanadi.", "Sabrsizlar yutqazadi.",
    "Qiyinchilik — vaqtinchalik mehmon.", "Sen o‘zingni kashf qilmagansan hali.", "Har kuni o‘z ustingda ishlagin.",
    "Yutuq — chidamlilik mevasidir.", "Sen o‘zingni cheklayapsan.", "O‘zingga imkon ber.",
    "Eng katta tavakkal — urinmaslik.", "Qo‘rquv seni to‘xtatmasin.", "Sen o‘zingni o‘zgartira olasan.",
    "Bugun boshlagan odam ertaga yutadi.", "Hech qachon kech emas.", "Harakat qil — natija keladi.",
    "Sen kuchsiz emassan — charchagansan xolos.", "Dam ol, lekin taslim bo‘lma.", "Har kuni 1% yaxshilan.",
    "Qanchalik qiynalsang, shunchalik qadrlaysan.", "Sen bunga arziysan.", "O‘z hayotingni o‘zgartir.",
    "Yutuq oson kelmaydi.", "Harakat qilmaslik — eng katta xato.", "Sen o‘zingni sinab ko‘r.",
    "Orzular — jasurlarga tegishli.", "Sen hali imkoniyatlaringni ishlatmading.", "O‘zingga sodiq bo‘l.",
    "Qiyin yo‘l — to‘g‘ri yo‘l bo‘lishi mumkin.", "Taslim bo‘lish — variant emas.", "Sen yutishga yaratilgansan.",
    "Harakat qil — sharoit o‘zgaradi.", "Sen boshlagan ishni tugat.", "Eng zo‘r vaqt — hozir.",
    "O‘zgarish sendan boshlanadi.", "Sen kuchli bo‘lishni tanla.", "O‘zingni o‘zing motivatsiya qil.",
    "Har kuni yangi imkon.", "Sen hali eng yaxshisini ko‘rmading.", "O‘z yo‘lingni tanla va yur.",
    "Sen bunga qodirsan — ishon.", "Harakat qilgan odam yutadi.", "Qanchalik qiyin bo‘lsa — shunchalik qiymatli.",
    "Sen hech qachon yolg‘iz emassan — o‘zing bor.", "Boshlagin. Hozir. Shu yerda.", "G'alaba intizomni sevadi."
]

GIFS = [
    "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3eXJqM3Z4eXp5bmZ6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6JmR6PTEmZ3R6Z3R6/3o7TKDkDbIDJieKbVm/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOTVkZ3hueXBnNjkwZ2J1YjJkN2gwMHN3b3M3aXZ0cnRvMDFpbHdkZyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/FACfMgP1N9mlG/giphy.gif"
]

def get_user_stats(uid):
    if uid not in user_data:
        user_data[uid] = {'daily_count': 0, 'history': [], 'total_days': 0}
    return user_data[uid]

def main_menu():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add(KeyboardButton("Bugungi vazifalar ✅"), KeyboardButton("Natijalar jadvali 🏆"), KeyboardButton("Finish 🏁"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    get_user_stats(message.chat.id)
    bot.send_message(message.chat.id, "<b>30 kunlik challenge boshlandi!</b> 🔥", parse_mode='HTML', reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == "Bugungi vazifalar ✅")
def show_tasks(message):
    uid = message.chat.id
    stats = get_user_stats(uid)
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for task in DAILY_TASKS:
        markup.add(KeyboardButton(task))
    markup.add(KeyboardButton("Orqaga ⬅️"))
    bot.send_message(uid, f"📊 Progress: {stats['daily_count']}/{len(DAILY_TASKS)}\n👇 Vazifani tanlang:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in DAILY_TASKS)
def complete_task(message):
    uid = message.chat.id
    stats = get_user_stats(uid)
    stats['daily_count'] += 1
    bot.send_message(uid, f"✅ Bajarildi! ({stats['daily_count']}/{len(DAILY_TASKS)})")

@bot.message_handler(func=lambda m: m.text == "Finish 🏁")
def finish_day(message):
    uid = message.chat.id
    stats = get_user_stats(uid)
    
    if stats['daily_count'] == 0:
        bot.send_message(uid, "Hali birorta ham vazifa bajarmadingiz-ku? 🤨")
        return

    percent = int((stats['daily_count'] / len(DAILY_TASKS)) * 100)
    stats['total_days'] += 1
    
    # Motivatsiya tanlash
    motivation = random.choice(MOTIVATIONS)

    if percent == 100:
        msg = f"🏆 **DAHAXSHAT! 100% Natija!**\n\n{motivation}\n\nSen bilan faxrlanaman! ✊"
        bot.send_animation(uid, random.choice(GIFS), caption=msg, parse_mode='Markdown')
    elif percent >= 70:
        msg = f"📈 **Yaxshi natija: {percent}%**\n\n{motivation}\n\nErtaga 100% kutaman! ✨"
        bot.send_message(uid, msg, parse_mode='Markdown')
    else:
        msg = f"⚠️ **Natija: {percent}%**\n\n{motivation}\n\nHali imkoniyat bor, bo'shashma! 🔥"
        bot.send_message(uid, msg, parse_mode='Markdown')

    stats['history'].append(f"📅 {stats['total_days']}-kun: {percent}% ({stats['daily_count']}/7)")
    stats['daily_count'] = 0 
    bot.send_message(uid, "Kun yopildi. Ertaga yangi g'alabalar kutmoqda!", reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == "Natijalar jadvali 🏆")
def show_leaderboard(message):
    uid = message.chat.id
    stats = get_user_stats(uid)
    if not stats['history']:
        msg = "Jadval hozircha bo'sh. Kunni yakunlang! 🚀"
    else:
        msg = "🏆 **SIZNING 30 KUNLIK PROGRESSINGIZ:**\n\n" + "\n".join(stats['history'])
    bot.send_message(uid, msg, parse_mode='Markdown')

@bot.message_handler(func=lambda m: m.text == "Orqaga ⬅️")
def back(message):
    bot.send_message(message.chat.id, "Asosiy menyu:", reply_markup=main_menu())

bot.infinity_polling()
