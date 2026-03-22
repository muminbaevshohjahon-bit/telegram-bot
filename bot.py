import telebot
import os
import random
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from apscheduler.schedulers.background import BackgroundScheduler

# Railway Variables
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# Foydalanuvchilar ro'yxati
users_list = set()

# 1. 100 TA MOTIVATSIYA (Xatosiz yopilgan qatorlar bilan)
MOTIVATIONS = [
    "Sen boshlamasang, hech narsa boshlanmaydi.", "Mukammallikni kutma — harakatni boshlash muhim.",
    "Bugungi og‘riq — ertangi kuch.", "Sen o‘ylagandan ham kuchlisan.",
    "Hech kim seni qutqarmaydi — o‘zingni o‘zing ko‘tar.", "Qiyinchilik — bu yashirin imkoniyat.",
    "Orzular faqat harakat bilan haqiqatga aylanadi.", "Qo‘rqish — o‘sish boshlanishidir.",
    "Har kuni kichik qadam — katta natija.", "Sen taslim bo‘lmaguningcha, yutqazmading.",
    "Eng katta raqibing — kechagi o‘zing.", "Bahonalar seni orqaga tortadi.",
    "Harakat — motivatsiyadan muhimroq.", "Vaqt ketmoqda — senchi?",
    "Sen bunga loyiqsan — lekin ishlashing kerak.", "Og‘ir bo‘lsa ham davom et.",
    "O‘zgarish og‘riqli, lekin zarur.", "Qanchalik qiynalsang, shunchalik kuchli bo‘lasan.",
    "Natija sabrni yaxshi ko‘radi.", "Bugun qilmaganing — ertaga pushaymon bo‘ladi.",
    "Sen o‘zingning hayoting uchun javobgarsan.", "Kichik boshlashdan uyalmagin.",
    "Har kuni o‘zingni yeng.", "Kuch — ichingda. Uni uyg‘ot.",
    "Taslim bo‘lish — eng oson yo‘l.", "Eng yaxshi vaqt — hozir.",
    "Qancha ko‘p harakat, shuncha kam pushaymon.", "Qiyinchilik seni sinaydi, sindirmaydi.",
    "Yutuq — intizom natijasi.", "Orzularing seni kutmaydi.",
    "Qo‘rquv ortida — erkinlik bor.", "Hech kim senga majbur emas — o‘zingni isbotla.",
    "Harakat qil, hatto mukammal bo‘lmasa ham.", "Yiqildingmi? Tur va davom et.",
    "Sen hali boshlamading ham.", "Qanchalik ko‘p urinma, shunchalik yaqinlashasan.",
    "Og‘riq vaqtinchalik — natija abadiy.", "Bugungi mehnat — ertangi faxr.",
    "Sen o‘zingni o‘zgartirsang, hayoting o‘zgarari.", "Kuchli bo‘lish — tanlov.",
    "Intizom — erkinlik kaliti.", "Qachon qiyin bo‘lsa — o‘sha payt o‘sasan.",
    "Orqaga emas, oldinga qaragin.", "Hech kim mukammal emas — lekin harakat qilayotganlar yutadi.",
    "O‘z ustingda ishlash — eng yaxshi investitsiya.", "Sen bunga qodirsan.",
    "Kech emas — hali vaqt bor.", "Boshlash — yarim g‘alaba.",
    "Kuchli odamlar bahona qilmaydi.", "Har kuni yangi imkoniyat.",
    "Sen taslim bo‘lsang — hammasi tugaydi.", "Sen davom etsang — hammasi boshlanadi.",
    "O‘z yo‘lingni o‘zing yarat.", "Orzularing seni chaqiryapti.",
    "Qadam tashla — yo‘l ochiladi.", "O‘zinga ishongan odam yutadi.",
    "Harakat qil, hatto sekin bo‘lsa ham.", "Katta natija — kichik odatlardan boshlanadi.",
    "Sabrsizlar yutqazadi.", "Qiyinchilik — vaqtinchalik mehmon.",
    "Sen o‘zingni kashf qilmagansan hali.", "Har kuni o‘z ustingda ishlagin.",
    "Yutuq — chidamlilik mevasidir.", "Sen o‘zingni cheklayapsan.",
    "O‘zingga imkon ber.", "Eng katta tavakkal — urinmaslik.",
    "Qo‘rquv seni to‘xtatmasin.", "Sen o‘zingni o‘zgartira olasan.",
    "Bugun boshlagan odam ertaga yutadi.", "Hech qachon kech emas.",
    "Harakat qil — natija keladi.", "Sen kuchsiz emassan — charchagansan xolos.",
    "Dam ol, lekin taslim bo‘lma.", "Har kuni 1% yaxshilan.",
    "Qanchalik qiynalsang, shunchalik qadrlaysan.", "Sen bunga arziysan.",
    "O‘z hayotingni o‘zgartir.", "Yutuq oson kelmaydi.",
    "Harakat qilmaslik — eng katta xato.", "Sen o‘zingni sinab ko‘r.",
    "Orzular — jasurlarga tegishli.", "Sen hali imkoniyatlaringni ishlatmading.",
    "O‘zingga sodiq bo‘l.", "Qiyin yo‘l — to‘g‘ri yo‘l bo‘lishi mumkin.",
    "Taslim bo‘lish — variant emas.", "Sen yutishga yaratilgansan.",
    "Harakat qil — sharoit o‘zgaradi.", "Sen boshlagan ishni tugat.",
    "Eng zo‘r vaqt — hozir.", "O‘zgarish sendan boshlanadi.",
    "Sen kuchli bo‘lishni tanla.", "O‘zingni o‘zing motivatsiya qil.",
    "Har kuni yangi imkon.", "Sen hali eng yaxshisini ko‘rmading.",
    "O‘z yo‘lingni tanla va yur.", "Sen bunga qodirsan — ishon.",
    "Harakat qilgan odam yutadi.", "Qanchalik qiyin bo‘lsa — shunchalik qiymatli.",
    "Sen hech qachon yolg‘iz emassan — o‘zing bor.", "Boshlagin. Hozir. Shu yerda."
]

# 2. ZAMONAVIY VA KUCHLI ESLATMALAR
REMINDERS = {
    "morning": [
        "Hoy qayerdasan? Chellenjlar oson yuzni borib yuvishdan ko'ra:) 🧼",
        "Chellenjlar sizni kutmoqda voy e! Tur o'rningdan! 🏃‍♂️",
        "Bugun seni yengadigan tong bo'lsin! Qani, boshladik! ✨"
    ],
    "afternoon": [
        "Qani bo'la qoling... Bilaman qorin och, lekin chellenjlar qolib ketmasin! 🥗",
        "Siz hozir nima qilayabsiz? Aytaymi, kitob o'qimoqchisiz? 😉 📖",
        "Energiyani tushirmang! Orzular uchun hozir ayni vaqti! 🔥"
    ],
    "evening": [
        "Uxlash oson! Orzular orzuligicha qolmasin :) ✨",
        "Hali imkoniyat bor! Orzularing seni kutmoqda. 🔥",
        "Shirin tushlarga bilet olishdan oldin hamma vazifani yopamiz! 🎫",
        "Kuning qanday o'tdi? Finishni bosishga tayyormisan? ✅"
    ]
}

# 3. SAMIMIY TABRIKLAR VA GIF-LAR
CONGRATS = [
    "Biz kutgandik, bilgandik shunday bo'lishini! 🌟",
    "Porloq kelajak seni qo'lingda! ✨",
    "Sen bilan faxrlanaman! ✊",
    "Malades! Mana bu haqiqiy natija! 🔥"
]

GIFS = [
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExeTVrZWJ3cWU2MDgzbTV3NGk5NWtocnNwdGJvd2cxMnJwMTRtN2RhYSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/3oEduUGL2JaSK7oS76/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3eW1hbnAyazN6OTRqa2R5ZHYyb250eHI4aW5zODFzZm0zOGFpOGt0NyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/ahDOY7XwxjNXW/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOTVkZ3hueXBnNjkwZ2J1YjJkN2gwMHN3b3M3aXZ0cnRvMDFpbHdkZyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/FACfMgP1N9mlG/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3ZTc5MnQxOTdhY3dnMWpuNXFmdzJ0dnR1Z29hMGV4cnVnaXp1YmtqbiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/IHETYBuNarfOwyDBrY/giphy.gif"
]

def send_periodic_msg(period):
    msg = random.choice(REMINDERS[period])
    for uid in list(users_list):
        try:
            bot.send_message(uid, f"🔔 **ESLATMA:**\n\n{msg}", parse_mode='Markdown')
        except: pass

# Scheduler (Siz aytgan vaqt oralig'ida random xabarlar yuboradi)
scheduler = BackgroundScheduler()
scheduler.add_job(send_periodic_msg, 'cron', hour=8, minute=0, args=['morning'])
scheduler.add_job(send_periodic_msg, 'cron', hour=14, minute=0, args=['afternoon'])
scheduler.add_job(send_periodic_msg, 'cron', hour=21, minute=0, args=['evening'])
scheduler.start()

@bot.message_handler(commands=['start'])
def start(message):
    users_list.add(message.chat.id)
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(KeyboardButton("Bugungi vazifalar ✅"), KeyboardButton("Natijalar jadvali 🏆"), KeyboardButton("Finish 🏁"))
    welcome_text = "<b>30 kunlik challenge'ga xush kelibsiz!</b> 🔥\n\n<i>Bu bot MBE Useful tomonidan yaratilgan.</i>"
    bot.send_message(message.chat.id, welcome_text, parse_mode='HTML', reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "Bugungi vazifalar ✅")
def show_tasks(message):
    motivation = random.choice(MOTIVATIONS)
    bot.send_message(message.chat.id, f"💡 **Kun motivatsiyasi:**\n'{motivation}'\n\nVazifalarni boshlang!")

@bot.message_handler(func=lambda m: "✅" in m.text and m.text != "Bugungi vazifalar ✅")
def task_done(message):
    # Har bir topshiriqdan keyin random tabrik va GIF
    txt = random.choice(CONGRATS)
    gif = random.choice(GIFS)
    bot.send_animation(message.chat.id, gif, caption=f"✨ {txt}")

bot.infinity_polling()
