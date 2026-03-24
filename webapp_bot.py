Endi Web.app qismini ishlaymiz! import telebot
import os
import random
import json
import threading
import time
from datetime import datetime
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

# Vaqt zonasi
os.environ['TZ'] = 'Asia/Tashkent'
if hasattr(time, 'tzset'):
    time.tzset()

TOKEN =Endi Web.app qismini ishlaymiz! import telebot
import os
import random
import json
import threading
import time
from datetime import datetime
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

# Vaqt zonasi
os.environ['TZ'] = 'Asia/Tashkent'
if hasattr(time, 'tzset'):
    time.tzset()

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# --- ADMIN ID ---
# O'zingizning ID raqamingizni kiriting
ADMIN_ID = 6338204692 

# --- MA'LUMOTLAR ---
def load_data():
    try:
        with open('users_db.json', 'r') as f:
            return json.load(f)
    except:
        return {}
        
def save_data():
    with open('users_db.json', 'w') as f:
        json.dump(user_data, f, indent=4)

user_data = load_data()
TOTAL_TASKS = 7

# MOTIVATSIYALAR
CUSTOM_MOTIVATIONS = [
    "Sen boshlamasang, hech narsa boshlanmaydi. 🔥", "Bugungi og‘riq — ertangi kuch. 💪",
    "Eng zo‘r vaqt — hozir. 🚀", "Intizom — bu o'ziga berilgan va'dani bajarishdir. ✨",
    "Har kuni kichik qadam — katta natija.", "Eng katta raqibing — kechagi o‘zing.",
    "Mukammallikni kutma — harakatni boshlash muhim.", "Sen o‘ylagandan ham kuchlisan.",
    "Hech kim seni qutqarmaydi — o‘zingni o‘zing ko‘tar.", "Qiyinchilik — bu yashirin imkoniyat.",
    "Orzular faqat harakat bilan haqiqatga aylanadi.", "Qo‘rqish — o‘sish boshlanishidir.",
    "Sen taslim bo‘lmaguningcha, yutqazmading.", "Bahonalar seni orqaga tortadi.",
    "Harakat — motivatsiyadan muhimroq.", "Vaqt ketmoqda — senchi?",
    "O‘zgarish og‘riqli, lekin zarur.", "Natija sabrni yaxshi ko‘radi.",
    "Bugun qilmaganing — ertaga pushaymon bo‘ladi.", "Kichik boshlashdan uyalmagin.",
    "Eng katta tavakkal — urinmaslik.", "Qo‘rquv seni to‘xtatmasin.",
    "O‘zingga sodiq bo‘l.", "Taslim bo‘lish — variant emas.",
    "O‘zgarish sendan boshlanadi.", "Boshlagin. Hozir. Shu yerda.",
    "Aqilli inson uchun har kuni yangi kun boshlanadi.","Kuchsizlar faqat taslim bo'ladi."
]

FINISH_MOTIVATIONS = [
    "Dahshat! Vapshe zo'r, barakalla! 🔥",
    "Sen o'ylagandan ham kuchlisan, davom et! 💪",
    "Intizom — bu o'zingga bo'lgan hurmat. 🌟",
    "Bo'lar ekanku, senga ishonaman!",
    "Bo'shashma zo'r ketayabsan",
    "Ko'zim to'rt bo'lib ketdi, malades."
]

GIFS = [
    "https://media.giphy.com/media/FACfMgP1N9mlG/giphy.gif",
    "https://media2.giphy.com/media/fUQ4rhUZJYiQsas6WD/giphy.gif",
    "https://media.giphy.com/media/tHIRLHtNwxpjIFqPdV/giphy.gif",
    "https://media.giphy.com/media/8ZblO3ZD5NMltPaFS2/giphy.gif",
    "https://media.giphy.com/media/g9582DNuQppxC/giphy.gif"
]

def get_user(uid):
    uid = str(uid)
    if uid not in user_data:
        user_data[uid] = {'total_score': 0, 'history': [], 'completed_today': [], 'info': {}, 'step': 'start'}
    return user_data[uid]

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    web_url = f"https://muminbaevshohjahon-bit.github.io/telegram-bot/?v={random.randint(1, 999999)}"
    markup.add(KeyboardButton("Chellenjlar 🗓", web_app=WebAppInfo(url=web_url)))
    markup.add(KeyboardButton("Peshqadamlar 🏆"), KeyboardButton("Mening natijam 📊"))
    markup.add(KeyboardButton("Finish 🏁"))
    return markup

# --- START VA REGISTRATSIYA ---
@bot.message_handler(commands=['start'])
def start(message):
    uid = str(message.chat.id)
    user_data[uid] = {'total_score': 0, 'history': [], 'completed_today': [], 'info': {}, 'step': 'get_name'}
    save_data()
    welcome_text = (
        "<b><i>Assalomu aleykum hush kelibsiz!</i></b>\n"
        "<b><i>Men MBE useful tomonidan yaratilgan botman!</i></b>\n\n"
        "<b><i>Maqsadimiz 30 kunlik chellenj davomida intizomni shakllantirish.</i></b>\n\n"
        "Keling tanishib olaylik... Ismingizni kiriting:"
    )
    bot.send_message(uid, welcome_text, parse_mode='HTML')

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_name')
def get_name(message):
    uid = str(message.chat.id)
    user_data[uid]['info']['name'] = message.text
    user_data[uid]['step'] = 'get_year'
    save_data()
    bot.send_message(message.chat.id, "Tug‘ilgan yilingiz (masalan: 2004):")

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_year')
def get_year(message):
    uid = str(message.chat.id)
    user_data[uid]['info']['birth_year'] = message.text
    user_data[uid]['step'] = 'get_month'
    save_data()
    bot.send_message(message.chat.id, "Tug‘ilgan oyingiz (masalan: Avgust):")

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_month')
def get_month(message):
    uid = str(message.chat.id)
    user_data[uid]['info']['birth_month'] = message.text
    user_data[uid]['step'] = 'get_day'
    save_data()
    bot.send_message(message.chat.id, "Tug‘ilgan kuningiz (masalan: 25):")

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_day')
def get_day(message):
    uid = str(message.chat.id)
    user_data[uid]['info']['birth_day'] = message.text
    user_data[uid]['step'] = 'get_nick'
    save_data()
    bot.send_message(message.chat.id, "Nickname kiriting:")

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_nick')
def get_nick(message):
    uid = str(message.chat.id)
    user_data[uid]['info']['nickname'] = message.text
    user_data[uid]['step'] = 'main'
    save_data()
    bot.send_message(message.chat.id, "Tabrikleyshn, Ro'yxatdan o'tildi!🔥", reply_markup=main_menu())

# --- ADMIN PANEL FUNKSIYALARI ---
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.chat.id == ADMIN_ID: 
        total = len(user_data)
        text = f"👨‍💻 <b>Admin Panel</b>\n\n👥 Jami foydalanuvchilar: {total}\n\n/users - Ro'yxat\n/db_download - Bazani yuklab olish"
        bot.send_message(message.chat.id, text, parse_mode='HTML')

@bot.message_handler(commands=['users'])
def list_users(message):
    if message.chat.id == ADMIN_ID:
        text = "📋 <b>Foydalanuvchilar:</b>\n\n"
        for uid, data in user_data.items():
            name = data.get('info', {}).get('name', "Noma'lum")
            nick = data.get('info', {}).get('nickname', "Yo'q")
            score = data.get('total_score', 0)
            text += f"👤 {name} (@{nick}) — {score} ball\n"
        bot.send_message(message.chat.id, text, parse_mode='HTML')

@bot.message_handler(commands=['db_download'])
def send_db(message):
    if message.chat.id == ADMIN_ID:
        try:
            with open('users_db.json', 'rb') as f:
                bot.send_document(message.chat.id, f)
        except:
            bot.send_message(message.chat.id, "Baza fayli topilmadi.")

# --- PESHQADAMLAR ---
@bot.message_handler(func=lambda m: m.text == "Peshqadamlar 🏆")
def leaderboard(message):
    users = []
    
    # 1. Ma'lumotlarni yig'ish (Sizning kodingiz)
    for uid, data in user_data.items():
        score = data.get('total_score', 0)
        # Bu yerda foydalanuvchini ro'yxatga qo'shamiz
        users.append({'uid': uid, 'score': score})

    # 2. Saralash (Ballar bo'yicha yuqoridan pastga)
    users = sorted(users, key=lambda x: x['score'], reverse=True)

    # 3. Matnni shakllantirish (Siz so'ragan qator shu yerda)
    text = "🏆 **Peshqadamlar jadvali:**\n\n"
    
    for i, u in enumerate(users[:10], 1):  # Top 10 talik
        # MANA SHU QATORNI SHU YERGA QO'YING:
        text += f"{i}. ID: `{u['uid']}` — {u['score']} ball\n"

    # 4. Foydalanuvchiga yuborish
    if not users:
        text = "Hozircha hech kim ball to'plamadi."
        
    bot.send_message(message.chat.id, text, parse_mode='Markdown')
    
    if not users:
        bot.send_message(message.chat.id, "Hali hech kim ro'yxatdan o'tmagan.")
        return

    users.sort(key=lambda x: x['score'], reverse=True)
    text = "🏆 <b>Eng kuchli ishtirokchilar:</b>\n\n"
    for i, u in enumerate(users[:10], 1):
        text += f"{i}. {u['nick']} — {u['score']} ball\n"
    bot.send_message(message.chat.id, text, parse_mode='HTML')

# --- MENING NATIJAM ---
# --- MENING NATIJAM ---
@bot.message_handler(func=lambda m: m.text == "Mening natijam 📊")
def my_result(message):
    uid = str(message.chat.id)
    
    if uid not in user_data:
        bot.send_message(uid, "Siz hali ro'yxatdan o'tmagansiz. /start bosing.")
        return

    data = user_data[uid]
    name = data.get('info', {}).get('name', "Noma'lum")
    score = data.get('total_score', 0)
    
    # MANA SIZ YOZGAN KOD SHU YERDA:
    response_text = "📊 **Sizning natijangiz:**\n"
    response_text += f"""
👤 {name}
🆔 `{uid}`
🎂 {data['info'].get('birth_day', '??')}/{data['info'].get('birth_month', '??')}/{data['info'].get('birth_year', '????')}
⭐ {score} ball
"""
    
    # Qo'shimcha: Nechanchi kunda ekanligini ham qo'shib qo'yamiz
    current_day = data.get('current_day', 1)
    response_text += f"\n📅 Hozirgi kun: **{current_day}-kun**"

    bot.send_message(uid, response_text, parse_mode='Markdown')
# --- FINISH ---
@bot.message_handler(func=lambda m: m.text == "Finish 🏁")
def finish_day(message):
    user = get_user(message.chat.id)
    today = datetime.now().strftime('%d/%m')
    if any(today in entry for entry in user.get('history', [])):
        bot.send_message(message.chat.id, "Bugun yakunlab bo'lingan! ✨")
        return
    
    percent = int((len(user.get('completed_today', [])) / TOTAL_TASKS) * 100)
    user.setdefault('history', []).append(f"{today}: {percent}%")
    user['completed_today'] = []
    save_data()
    
    if percent >= 50:
        motivation = random.choice(FINISH_MOTIVATIONS)
        bot.send_animation(message.chat.id, random.choice(GIFS), caption=f"🏁 Natija: {percent}%\n\n{motivation}", parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, f" Natija: {percent}%\n\nErtaga kuchliroq bo'lamiz! 💪", parse_mode='HTML')

# --- SCHEDULER ---
def auto_scheduler():
    while True:
        now = datetime.now().strftime("%H:%M")
        if now == "08:00":
            for uid in list(user_data.keys()):
                try: bot.send_message(uid, "☀️ Xayrli tong! Bugun 7 ta vazifani ham yoramizmi?")
                except: pass
            time.sleep(61)
        if now == "21:00":
            for uid in list(user_data.keys()):
                try: bot.send_message(uid, "🔔 Kun yakunlanmoqda, Finish tugmasini bosishni unutmang!")
                except: pass
            time.sleep(61)
        if now == "23:00":
            today = datetime.now().strftime('%d/%m')
            for uid, data in user_data.items():
                if not any(today in entry for entry in data.get('history', [])):
                    completed = len(data.get('completed_today', []))
                    percent = int((completed / TOTAL_TASKS) * 100)
                    data.setdefault('history', []).append(f"{today}: {percent}%")
                    data['completed_today'] = []
            save_data()
            time.sleep(61)
        time.sleep(30)

threading.Thread(target=auto_scheduler, daemon=True).start()

# --- WEBAPP DATA ---
@bot.message_handler(content_types=['web_app_data'])
def web_app_receive(message):
    data = json.loads(message.web_app_data.data)
    user = get_user(message.chat.id)

    if data.get('action') == "done":
        task = data.get('task')

        if task not in user.get('completed_today', []):
            user.setdefault('completed_today', []).append(task)
            user['total_score'] += 10
            save_data()

            percent = int((len(user['completed_today']) / TOTAL_TASKS) * 100)

            if percent >= 20:
                bot.send_animation(
                    message.chat.id,
                    random.choice(GIFS),
                    caption=f"🔥 {task} bajarildi!\n+10 ball\n\n{random.choice(CUSTOM_MOTIVATIONS)}",
                    parse_mode='HTML'
                )
            else:
                bot.send_message(
                    message.chat.id,
                    f"✅ {task} bajarildi!\n+10 ball\n\n{random.choice(CUSTOM_MOTIVATIONS)}"
                )

if __name__ == "__main__":
    bot.infinity_polling()


<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Intizom Tracker</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f172a; color: white; padding: 15px; margin: 0; -webkit-user-select: none; }
        .streak-header { background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); padding: 15px; border-radius: 12px; text-align: center; margin-bottom: 20px; border: 1px solid #3b82f6; box-shadow: 0 4px 15px rgba(59, 130, 246, 0.2); }
        .card { background: #1e293b; padding: 15px; margin: 10px 0; border-radius: 12px; display: flex; justify-content: space-between; align-items: center; cursor: pointer; border: 1px solid transparent; transition: all 0.2s ease; }
        .card:active { transform: scale(0.98); background: #334155; }
        .grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 8px; margin-top: 15px; }
        .day { aspect-ratio: 1; display: flex; align-items: center; justify-content: center; border-radius: 8px; background: #1e293b; color: #475569; font-weight: bold; font-size: 14px; transition: 0.3s; }
        .done { background: #22c55e !important; color: white !important; box-shadow: 0 0 10px rgba(34, 197, 94, 0.4); }
        .active { border: 2px solid #facc15; color: white; background: #334155; }
        button { margin-top: 20px; width: 100%; padding: 15px; border: none; border-radius: 12px; background: #3b82f6; color: white; font-weight: bold; font-size: 16px; cursor: pointer; }
        button:active { background: #2563eb; }
    </style>
</head>
<body>

    <div class="streak-header">
        <h3 id="streakDisplay">🔥 Yuklanmoqda...</h3>
    </div>

    <div id="mainView">
        <h2 style="text-align: center;">🎯 Kunlik Vazifalar</h2>
        <div id="taskList"></div>
    </div>

    <div id="calendarView" style="display:none;">
        <h3 id="taskTitle" style="text-align: center; color: #38bdf8;"></h3>
        <div class="grid" id="grid"></div>
        <button onclick="showMain()">⬅️ Orqaga qaytish</button>
    </div>

    <script>
        const tg = window.Telegram.WebApp;
        tg.expand();

        // 1. URL parametrlaridan joriy kunni o'qib olish
        const urlParams = new URLSearchParams(window.location.search);
        const userDay = parseInt(urlParams.get('day')) || 1;

        document.getElementById("streakDisplay").innerText = `🔥 Siz ${userDay}-kundasiz`;

        const tasks = [
            "Tongda telefonsiz detox 1 soat 📱",
            "Shakarsiz hayot 🍰",
            "Kitob mutolasi 15 daqiqa 📚",
            "Gazsiz ichimliklar 🍵",
            "23:00 gacha uyqu 🌙",
            "Jismoniy faoliyat 🤾‍♀️",
            "2 daqiqa sukunat 🧘",
            "DEEP WORK 🧑‍🎓",
            "Kuniga 5000 so'm sarmoya 💸"
        ];

        function renderTasks() {
            const list = document.getElementById("taskList");
            list.innerHTML = "";
            tasks.forEach(task => {
                const div = document.createElement("div");
                div.className = "card";
                div.innerHTML = `<span>${task}</span><span>➡️</span>`;
                div.onclick = () => openCalendar(task);
                list.appendChild(div);
            });
        }

        function openCalendar(task) {
            document.getElementById("mainView").style.display = "none";
            document.getElementById("calendarView").style.display = "block";
            document.getElementById("taskTitle").innerText = task;

            const grid = document.getElementById("grid");
            grid.innerHTML = "";

            for (let i = 1; i <= 30; i++) {
                const dayDiv = document.createElement("div");
                dayDiv.className = "day";
                dayDiv.innerText = i;

                const key = `task_${task}_day_${i}`;
                if (localStorage.getItem(key) === "done") dayDiv.classList.add("done");

                if (i === userDay) {
                    dayDiv.classList.add("active");
                    dayDiv.onclick = () => {
                        if (!dayDiv.classList.contains("done")) {
                            handleTaskClick(dayDiv, task, i);
                        }
                    };
                } else {
                    dayDiv.onclick = () => tg.showAlert(`Siz hozircha faqat ${userDay}-kun vazifasini belgilay olasiz!`);
                }
                grid.appendChild(dayDiv);
            }
        }

        function handleTaskClick(el, taskName, dayNum) {
            if (taskName.includes("DEEP WORK")) {
                tg.showPopup({
                    title: 'Deep Work seansi',
                    message: 'Bugun necha soat chuqur diqqat bilan ishladingiz?',
                    buttons: [
                        {id: '1', type: 'default', text: '1-2 soat'},
                        {id: '2', type: 'default', text: '3-5 soat'},
                        {id: '3', type: 'default', text: '5+ soat'},
                        {id: 'cancel', type: 'destructive', text: 'Bekor qilish'}
                    ]
                }, (buttonId) => {
                    if (buttonId !== 'cancel') {
                        let hours = buttonId === '1' ? "1-2" : buttonId === '2' ? "3-5" : "5+";
                        completeTask(el, taskName, dayNum, hours);
                    }
                });
            } else {
                completeTask(el, taskName, dayNum);
            }
        }

        function completeTask(el, taskName, dayNum, extra = "") {
            const key = `task_${taskName}_day_${dayNum}`;
            el.classList.add("done");
            localStorage.setItem(key, "done");
            
            tg.HapticFeedback.impactOccurred('medium');
            
            // Botga yuboriladigan JSON ma'lumot
            tg.sendData(JSON.stringify({
                action: "done",
                task: taskName,
                day: dayNum,
                duration: extra 
            }));
        }

        function showMain() {
            document.getElementById("mainView").style.display = "block";
            document.getElementById("calendarView").style.display = "none";
        }

        renderTasks();
    </script>
</body>
</html>

# --- ADMIN ID ---
# O'zingizning ID raqamingizni kiriting
ADMIN_ID = 6338204692 

# --- MA'LUMOTLAR ---
def load_data():
    try:
        with open('users_db.json', 'r') as f:
            return json.load(f)
    except:
        return {}
        
def save_data():
    with open('users_db.json', 'w') as f:
        json.dump(user_data, f, indent=4)

user_data = load_data()
TOTAL_TASKS = 8

# MOTIVATSIYALAR
CUSTOM_MOTIVATIONS = [
    "Sen boshlamasang, hech narsa boshlanmaydi. 🔥", "Bugungi og‘riq — ertangi kuch. 💪",
    "Eng zo‘r vaqt — hozir. 🚀", "Intizom — bu o'ziga berilgan va'dani bajarishdir. ✨",
    "Har kuni kichik qadam — katta natija.", "Eng katta raqibing — kechagi o‘zing.",
    "Mukammallikni kutma — harakatni boshlash muhim.", "Sen o‘ylagandan ham kuchlisan.",
    "Hech kim seni qutqarmaydi — o‘zingni o‘zing ko‘tar.", "Qiyinchilik — bu yashirin imkoniyat.",
    "Orzular faqat harakat bilan haqiqatga aylanadi.", "Qo‘rqish — o‘sish boshlanishidir.",
    "Sen taslim bo‘lmaguningcha, yutqazmading.", "Bahonalar seni orqaga tortadi.",
    "Harakat — motivatsiyadan muhimroq.", "Vaqt ketmoqda — senchi?",
    "O‘zgarish og‘riqli, lekin zarur.", "Natija sabrni yaxshi ko‘radi.",
    "Bugun qilmaganing — ertaga pushaymon bo‘ladi.", "Kichik boshlashdan uyalmagin.",
    "Eng katta tavakkal — urinmaslik.", "Qo‘rquv seni to‘xtatmasin.",
    "O‘zingga sodiq bo‘l.", "Taslim bo‘lish — variant emas.",
    "O‘zgarish sendan boshlanadi.", "Boshlagin. Hozir. Shu yerda.",
    "Aqilli inson uchun har kuni yangi kun boshlanadi.","Kuchsizlar faqat taslim bo'ladi."
]

FINISH_MOTIVATIONS = [
    "Dahshat! Vapshe zo'r, barakalla! 🔥",
    "Sen o'ylagandan ham kuchlisan, davom et! 💪",
    "Intizom — bu o'zingga bo'lgan hurmat. 🌟",
    "Bo'lar ekanku, senga ishonaman!",
    "Bo'shashma zo'r ketayabsan",
    "Ko'zim to'rt bo'lib ketdi, malades."
]

GIFS = [
    "https://media.giphy.com/media/FACfMgP1N9mlG/giphy.gif",
    "https://media2.giphy.com/media/fUQ4rhUZJYiQsas6WD/giphy.gif",
    "https://media.giphy.com/media/tHIRLHtNwxpjIFqPdV/giphy.gif",
    "https://media.giphy.com/media/8ZblO3ZD5NMltPaFS2/giphy.gif",
    "https://media.giphy.com/media/g9582DNuQppxC/giphy.gif"
]

def get_user(uid):
    uid = str(uid)
    if uid not in user_data:
        user_data[uid] = {'total_score': 0, 'history': [], 'completed_today': [], 'info': {}, 'step': 'start'}
    return user_data[uid]

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    web_url = f"https://muminbaevshohjahon-bit.github.io/telegram-bot/?v={random.randint(1, 999999)}"
    markup.add(KeyboardButton("Chellenjlar 🗓", web_app=WebAppInfo(url=web_url)))
    markup.add(KeyboardButton("Peshqadamlar 🏆"), KeyboardButton("Mening natijam 📊"))
    markup.add(KeyboardButton("Finish 🏁"))
    return markup

# --- START VA REGISTRATSIYA ---
@bot.message_handler(commands=['start'])
def start(message):
    uid = message.chat.id

    if not check_sub(uid):
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📢 Kanalga obuna bo‘lish", url="https://t.me/mbe_useful"))
        markup.add(InlineKeyboardButton("✅ Tekshirish", callback_data="check_sub"))

        bot.send_message(uid, "❗ Iltimos, avval kanalga obuna bo‘ling!", reply_markup=markup)
        return

    user_data[str(uid)] = {
        'total_score': 0,
        'history': [],
        'completed_today': [],
        'info': {},
        'step': 'get_name',
        'user_id': random.randint(10000,99999),
        'streak': 0
    }
    save_data()
    @bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_sub_callback(call):
    uid = call.message.chat.id

    if check_sub(uid):
        bot.answer_callback_query(call.id, "✅ Tasdiqlandi!")
        start(call.message)
    else:
        bot.answer_callback_query(call.id, "❌ Hali obuna bo‘lmadingiz!", show_alert=True)

    bot.send_message(uid, "✅ Rahmat!.")

    welcome_text = (
        "<b>Assalomu alaykum!</b>\n\n"
        "MBE useful botiga xush kelibsiz,maqsadimiz 30 kunlik chellenj davomida intizomni shakllantirishi\n\n"
        "Ismingizni kiriting:"
    )
    bot.send_message(uid, welcome_text, parse_mode='HTML')
@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_name')
def get_name(message):
    uid = str(message.chat.id)
    user_data[uid]['info']['name'] = message.text
    user_data[uid]['step'] = 'get_year'
    save_data()
    bot.send_message(message.chat.id, "Tug‘ilgan yilingiz (masalan: 2004):")

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_year')
def get_year(message):
    uid = str(message.chat.id)
    user_data[uid]['info']['birth_year'] = message.text
    user_data[uid]['step'] = 'get_month'
    save_data()
    bot.send_message(message.chat.id, "Tug‘ilgan oyingiz (masalan: Avgust):")

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_month')
def get_month(message):
    uid = str(message.chat.id)
    user_data[uid]['info']['birth_month'] = message.text
    user_data[uid]['step'] = 'get_day'
    save_data()
    bot.send_message(message.chat.id, "Tug‘ilgan kuningiz (masalan: 25):")

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_day')
def get_day(message):
    uid = str(message.chat.id)
    user_data[uid]['info']['birth_day'] = message.text
    user_data[uid]['step'] = 'get_nick'
    save_data()
    bot.send_message(message.chat.id, "Nickname kiriting:")

@bot.message_handler(func=lambda m: get_user(m.chat.id).get('step') == 'get_nick')
def get_nick(message):
    uid = str(message.chat.id)
    user_data[uid]['info']['nickname'] = message.text
    user_data[uid]['step'] = 'main'
    save_data()
    bot.send_message(message.chat.id, "Tabrikleyshn, Ro'yxatdan o'tildi!🔥", reply_markup=main_menu())

# --- ADMIN PANEL FUNKSIYALARI ---
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.chat.id == ADMIN_ID: 
        total = len(user_data)
        text = f"👨‍💻 <b>Admin Panel</b>\n\n👥 Jami foydalanuvchilar: {total}\n\n/users - Ro'yxat\n/db_download - Bazani yuklab olish"
        bot.send_message(message.chat.id, text, parse_mode='HTML')

@bot.message_handler(commands=['users'])
def list_users(message):
    if message.chat.id == ADMIN_ID:
        text = "📋 <b>Foydalanuvchilar:</b>\n\n"
        for uid, data in user_data.items():
            name = data.get('info', {}).get('name', "Noma'lum")
            nick = data.get('info', {}).get('nickname', "Yo'q")
            score = data.get('total_score', 0)
            text += f"👤 {name} (@{nick}) — {score} ball\n"
        bot.send_message(message.chat.id, text, parse_mode='HTML')

@bot.message_handler(commands=['db_download'])
def send_db(message):
    if message.chat.id == ADMIN_ID:
        try:
            with open('users_db.json', 'rb') as f:
                bot.send_document(message.chat.id, f)
        except:
            bot.send_message(message.chat.id, "Baza fayli topilmadi.")

# --- PESHQADAMLAR ---
@bot.message_handler(func=lambda m: m.text == "Peshqadamlar 🏆")
def leaderboard(message):
    users = []
    for uid, data in user_data.items():
        if 'info' in data and 'nickname' in data['info']:
            users.append({'nick': data['info']['nickname'], 'score': data.get('total_score', 0)})
    
    if not users:
        bot.send_message(message.chat.id, "Hali hech kim ro'yxatdan o'tmagan.")
        return

    users.sort(key=lambda x: x['score'], reverse=True)
    text = "🏆 <b>Eng kuchli ishtirokchilar:</b>\n\n"
    for i, u in enumerate(users[:10], 1):
        text += f"{i}. {u['nick']} — {u['score']} ball\n"
    bot.send_message(message.chat.id, text, parse_mode='HTML')

# --- MENING NATIJAM ---
@bot.message_handler(func=lambda m: m.text == "Mening natijam 📊")
def my_stats(message):
    user = get_user(message.chat.id)
    history = user.get('history', [])
    stat_text = "📊 <b>Natijalar:</b>\n\n"
    if not history: stat_text += "Hali natija yo'q."
    else:
        for entry in history[-7:]:
            try:
                day, res = entry.split(": ")
                icon = "✅" if "100%" in res else "📈"
                stat_text += f"{icon} {day}: {res}\n"
            except: continue
    stat_text += f"\n🔥 Umumiy ball: {user.get('total_score', 0)}"
    bot.send_message(message.chat.id, stat_text, parse_mode='HTML')

# --- FINISH ---
@bot.message_handler(func=lambda m: m.text == "Finish 🏁")
def finish_day(message):
    uid = str(message.chat.id)
    user = get_user(uid)

    today = datetime.now().strftime('%d/%m')

    if any(today in entry for entry in user['history']):
        bot.send_message(uid, "Bugun yakunlab bo‘lingan!")
        return

    percent = int((len(user['completed_today']) / TOTAL_TASKS) * 100)

    user['history'].append(f"{today}: {percent}%")
    user['completed_today'] = []

    # STREAK
    if percent >= 50:
        user['streak'] += 1
    else:
        user['streak'] = 0

    save_data()

    # ranking
    sorted_users = sorted(user_data.items(), key=lambda x: x[1]['total_score'], reverse=True)
    rank = [i for i,(u,_) in enumerate(sorted_users,1) if u == uid][0]

    bot.send_animation(
        uid,
        random.choice(GIFS),
        caption=(
            f"🏁 Natija: {percent}%\n"
            f"🏆 O‘rningiz: {rank}\n"
            f"🔥 Streak: {user['streak']} kun\n\n"
            f"{random.choice(FINISH_MOTIVATIONS)}"
        ),
        parse_mode='HTML'
    )
# --- SCHEDULER ---
def auto_scheduler():
    sent_times = set()

    while True:
        now = datetime.now().strftime("%H:%M")

        if now in ["06:00","09:00","12:00","16:00","19:00"] and now not in sent_times:
            for uid in user_data:
                try:
                    bot.send_message(uid, f"🔥 {random.choice(CUSTOM_MOTIVATIONS)}")
                except:
                    pass
            sent_times.add(now)

        if now == "23:00":
            for uid, data in user_data.items():
                today = datetime.now().strftime('%d/%m')
                if not any(today in entry for entry in data['history']):
                    percent = int((len(data['completed_today']) / TOTAL_TASKS) * 100)
                    data['history'].append(f"{today}: {percent}%")
                    data['completed_today'] = []

                    try:
                        bot.send_message(uid, f"⏰ Avto yakun!\nNatija: {percent}%")
                    except:
                        pass

            save_data()

        time.sleep(30)

threading.Thread(target=auto_scheduler, daemon=True).start()

# --- WEBAPP DATA ---
@bot.message_handler(content_types=['web_app_data'])
def web_app_receive(message):
    data = json.loads(message.web_app_data.data)
    user = get_user(message.chat.id)
    if data.get('action') == "done":
        task = data.get('task')
        if task not in user.get('completed_today', []):
            user.setdefault('completed_today', []).append(task)
            user['total_score'] = user.get('total_score', 0) + 10
            save_data()
            bot.send_message(message.chat.id, f"✅ {task} bajarildi!\n{random.choice(CUSTOM_MOTIVATIONS)}")

if __name__ == "__main__":
    bot.infinity_polling()



Menda HTML kodi juda to'g'ri ishlayabdi sen tepadagi senariyni yuqorida yozgan kodimga joylashtirib ma'nosini o'zgartirmaagn holda Web.app ga yuklash uchun tayyor qilib ber 
pastda Html kod:

<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Intizom Tracker</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f172a; color: white; padding: 15px; margin: 0; -webkit-user-select: none; }
        .streak-header { background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); padding: 15px; border-radius: 12px; text-align: center; margin-bottom: 20px; border: 1px solid #3b82f6; box-shadow: 0 4px 15px rgba(59, 130, 246, 0.2); }
        .card { background: #1e293b; padding: 15px; margin: 10px 0; border-radius: 12px; display: flex; justify-content: space-between; align-items: center; cursor: pointer; border: 1px solid transparent; transition: all 0.2s ease; }
        .card:active { transform: scale(0.98); background: #334155; }
        .grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 8px; margin-top: 15px; }
        .day { aspect-ratio: 1; display: flex; align-items: center; justify-content: center; border-radius: 8px; background: #1e293b; color: #475569; font-weight: bold; font-size: 14px; transition: 0.3s; }
        .done { background: #22c55e !important; color: white !important; box-shadow: 0 0 10px rgba(34, 197, 94, 0.4); }
        .active { border: 2px solid #facc15; color: white; background: #334155; }
        button { margin-top: 20px; width: 100%; padding: 15px; border: none; border-radius: 12px; background: #3b82f6; color: white; font-weight: bold; font-size: 16px; cursor: pointer; }
        button:active { background: #2563eb; }
    </style>
</head>
<body>

    <div class="streak-header">
        <h3 id="streakDisplay">🔥 Yuklanmoqda...</h3>
    </div>

    <div id="mainView">
        <h2 style="text-align: center;">🎯 Kunlik Vazifalar</h2>
        <div id="taskList"></div>
    </div>

    <div id="calendarView" style="display:none;">
        <h3 id="taskTitle" style="text-align: center; color: #38bdf8;"></h3>
        <div class="grid" id="grid"></div>
        <button onclick="showMain()">⬅️ Orqaga qaytish</button>
    </div>

    <script>
        const tg = window.Telegram.WebApp;
        tg.expand();

        // 1. URL parametrlaridan joriy kunni o'qib olish
        const urlParams = new URLSearchParams(window.location.search);
        const userDay = parseInt(urlParams.get('day')) || 1;

        document.getElementById("streakDisplay").innerText = `🔥 Siz ${userDay}-kundasiz`;

        const tasks = [
            "Tongda telefonsiz detox 1 soat 📱",
            "Shakarsiz hayot 🍰",
            "Kitob mutolasi 15 daqiqa 📚",
            "Gazsiz ichimliklar 🍵",
            "23:00 gacha uyqu 🌙",
            "Jismoniy faoliyat 🤾‍♀️",
            "2 daqiqa sukunat 🧘",
            "DEEP WORK 🧑‍🎓",
            "Kuniga 5000 so'm sarmoya 💸"
        ];

        function renderTasks() {
            const list = document.getElementById("taskList");
            list.innerHTML = "";
            tasks.forEach(task => {
                const div = document.createElement("div");
                div.className = "card";
                div.innerHTML = `<span>${task}</span><span>➡️</span>`;
                div.onclick = () => openCalendar(task);
                list.appendChild(div);
            });
        }

        function openCalendar(task) {
            document.getElementById("mainView").style.display = "none";
            document.getElementById("calendarView").style.display = "block";
            document.getElementById("taskTitle").innerText = task;

            const grid = document.getElementById("grid");
            grid.innerHTML = "";

            for (let i = 1; i <= 30; i++) {
                const dayDiv = document.createElement("div");
                dayDiv.className = "day";
                dayDiv.innerText = i;

                const key = `task_${task}_day_${i}`;
                if (localStorage.getItem(key) === "done") dayDiv.classList.add("done");

                if (i === userDay) {
                    dayDiv.classList.add("active");
                    dayDiv.onclick = () => {
                        if (!dayDiv.classList.contains("done")) {
                            handleTaskClick(dayDiv, task, i);
                        }
                    };
                } else {
                    dayDiv.onclick = () => tg.showAlert(`Siz hozircha faqat ${userDay}-kun vazifasini belgilay olasiz!`);
                }
                grid.appendChild(dayDiv);
            }
        }

        function handleTaskClick(el, taskName, dayNum) {
            if (taskName.includes("DEEP WORK")) {
                tg.showPopup({
                    title: 'Deep Work seansi',
                    message: 'Bugun necha soat chuqur diqqat bilan ishladingiz?',
                    buttons: [
                        {id: '1', type: 'default', text: '1-2 soat'},
                        {id: '2', type: 'default', text: '3-5 soat'},
                        {id: '3', type: 'default', text: '5+ soat'},
                        {id: 'cancel', type: 'destructive', text: 'Bekor qilish'}
                    ]
                }, (buttonId) => {
                    if (buttonId !== 'cancel') {
                        let hours = buttonId === '1' ? "1-2" : buttonId === '2' ? "3-5" : "5+";
                        completeTask(el, taskName, dayNum, hours);
                    }
                });
            } else {
                completeTask(el, taskName, dayNum);
            }
        }

        function completeTask(el, taskName, dayNum, extra = "") {
            const key = `task_${taskName}_day_${dayNum}`;
            el.classList.add("done");
            localStorage.setItem(key, "done");
            
            tg.HapticFeedback.impactOccurred('medium');
            
            // Botga yuboriladigan JSON ma'lumot
            tg.sendData(JSON.stringify({
                action: "done",
                task: taskName,
                day: dayNum,
                duration: extra 
            }));
        }

        function showMain() {
            document.getElementById("mainView").style.display = "block";
            document.getElementById("calendarView").style.display = "none";
        }

        renderTasks();
    </script>
</body>
</html>




