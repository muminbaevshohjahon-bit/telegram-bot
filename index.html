<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>MBE Useful - Kabinet</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        :root { --bg: #1c1c1e; --card: #2c2c2e; --accent: #34c759; --text: #ffffff; --warn: #ff3b30; }
        body { font-family: -apple-system, system-ui, sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 15px; }
        .tab-btn { background: var(--card); border: 1px solid #3a3a3c; color: white; padding: 10px; border-radius: 10px; flex: 1; margin: 5px; }
        .tab-btn.active { border-color: var(--accent); color: var(--accent); }
        .challenge-card { background: var(--card); padding: 18px; border-radius: 15px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; border: 1px solid #3a3a3c; }
        .calendar-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; margin-top: 15px; }
        .day-box { aspect-ratio: 1; background: var(--card); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 14px; border: 1px solid #3a3a3c; opacity: 0.5; }
        .day-box.active-day { opacity: 1; border-color: var(--accent); box-shadow: 0 0 5px var(--accent); }
        .day-box.done { background: var(--accent); color: black; opacity: 1; border: none; }
        .back-btn { background: var(--card); color: white; border: none; padding: 12px; border-radius: 10px; width: 100%; margin-bottom: 15px; }
        #leaderboardView, #calendarView { display: none; }
    </style>
</head>
<body>

    <div id="mainView">
        <div style="display: flex;">
            <button class="tab-btn active">Chellenjlar</button>
            <button class="tab-btn" onclick="showView('leaderboardView')">Reyting 📊</button>
        </div>
        <h3 style="margin-top: 20px;">Vazifalar:</h3>
        <div id="challengeList"></div>
    </div>

    <div id="calendarView">
        <button class="back-btn" onclick="showView('mainView')">⬅️ Orqaga</button>
        <h2 id="calTitle">Vazifa</h2>
        <p id="timeWarning" style="color: var(--warn); font-size: 12px;"></p>
        <div class="calendar-grid" id="calendarGrid"></div>
    </div>

    <div id="leaderboardView">
        <button class="back-btn" onclick="showView('mainView')">⬅️ Orqaga</button>
        <h2>🏆 Top Ishtirokchilar</h2>
        <div id="rankData" style="background: var(--card); padding: 15px; border-radius: 15px;">
            Yuklanmoqda...
        </div>
    </div>

    <script>
        const tg = window.Telegram.WebApp;
        tg.expand();

        const challenges = ["Kitob mutolasi 📚", "Jismoniy mashq 💪", "Sugar detox 🍬", "Gazsiz ichimliklar 🥤", "5000 so'm sarmoya 💰", "1 daqiqa sukunat 🧘‍♂️"];
        const today = new Date().getDate(); 
        const hour = new Date().getHours();

        function showView(viewId) {
            ['mainView', 'calendarView', 'leaderboardView'].forEach(v => document.getElementById(v).style.display = 'none');
            document.getElementById(viewId).style.display = 'block';
        }

        function initMain() {
            const list = document.getElementById('challengeList');
            list.innerHTML = '';
            challenges.forEach(ch => {
                const card = document.createElement('div');
                card.className = 'challenge-card';
                card.innerHTML = `<span>${ch}</span><span>➡️</span>`;
                card.onclick = () => openCalendar(ch);
                list.appendChild(card);
            });
        }

        function openCalendar(name) {
            showView('calendarView');
            document.getElementById('calTitle').innerText = name;
            const grid = document.getElementById('calendarGrid');
            grid.innerHTML = '';

            const isLate = hour >= 23;
            document.getElementById('timeWarning').innerText = isLate ? "Soat 23:00 dan o'tdi. Bugunni belgilash yopilgan!" : "Bugungi vazifa uchun faqat joriy kunni belgilang.";

            for (let i = 1; i <= 30; i++) {
                const day = document.createElement('div');
                day.className = 'day-box';
                day.innerText = i;
                
                if (i === today) day.classList.add('active-day');

                const key = `ch_${name}_day_${i}`;
                if (localStorage.getItem(key)) day.classList.add('done');

                day.onclick = () => {
                    if (i !== today) {
                        tg.showAlert("Faqat bugungi kunni belgilashingiz mumkin!");
                        return;
                    }
                    if (isLate) {
                        tg.showAlert("Kech qoldingiz! Vazifalar 23:00 gacha qabul qilinadi.");
                        return;
                    }
                    if (!day.classList.contains('done')) {
                        day.classList.add('done');
                        localStorage.setItem(key, 'true');
                        // Botga xabar yuborish
                        tg.sendData(JSON.stringify({action: "task_done", task: name}));
                    }
                };
                grid.appendChild(day);
            }
        }

        initMain();
    </script>
</body>
</html>
