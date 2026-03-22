# --- BOTGA QO'SHILADIGAN QISM ---

@bot.message_handler(content_types=['web_app_data'])
def web_app_receive(message):
    import json
    data = json.loads(message.web_app_data.data)
    
    if data.get('action') == "task_done":
        user = get_user(message.chat.id)
        task = data.get('task')
        
        # Ball berish
        user['total_score'] += 10
        save_data()
        
        # Motivatsiya yuborish
        mots = [
            f"🔥 Dahshat! {task} bajarildi. Davom et!",
            f"💪 Intizom — bu o'ziga berilgan va'dani bajarishdir. {task} uchun +10 ball!",
            f"🌟 Siz bugun kechagidan yaxshiroqsiz! {task} ro'yxatga olindi."
        ]
        bot.send_message(message.chat.id, random.choice(mots))

# Finish tugmasi bosilganda boshqa narsani bloklash uchun:
@bot.message_handler(func=lambda m: m.text == "Finish 🏁")
def finish_day(message):
    user = get_user(message.chat.id)
    # Bugun allaqachon finish bosilgan bo'lsa
    last_date = datetime.now().strftime('%d/%m')
    if any(last_date in entry for entry in user['history']):
        bot.send_message(message.chat.id, "Bugun uchun allaqachon yakunlagansiz. Ertagacha dam oling! ✨")
        return
    
    # ... (oldingi finish kodi)
