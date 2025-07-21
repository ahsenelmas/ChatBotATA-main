document.addEventListener('DOMContentLoaded', function () {
    const chatBox = document.getElementById('chatBox');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    const chatContainer = document.querySelector('.chat-wrapper');
    const announcementPanel = document.getElementById('announcementList');
    const announcementIcon = document.getElementById('announcementIcon');
    const announcementPopup = document.getElementById('announcementPopup');
    const closePopup = document.getElementById('closePopup');
    const popupTitle = document.getElementById('popupTitle');
    const popupContent = document.getElementById('popupContent');
    const popupPublish = document.getElementById('popupPublish');
    const announcementsList = document.getElementById('announcements');
    const languageSelect = document.getElementById('languageSelect');
    const exitButton = document.getElementById('exitButton');

    let currentMode = "";
    let lang = 'en';

    const translations = {
        en: {
            sendPlaceholder: "Type your question...",
            toastProfessor: "You're in Professor mode now.",
            toastDean: "You're in Dean mode now.",
            toastStudent: "You're in Student mode now.",
            toastEmpty: "Please fill all fields.",
            overlayProfessor: "Professor Mode Active",
            overlayDean: "Dean Mode Active",
            overlayStudent: "Student Mode: Welcome!",
            schedule: "📅 Weekly Schedule:\nMon - Math 10:00\nTue - Physics 12:00\nWed - AI 09:00\nFri - Literature 11:00",
            motivation: "🌟 Stay strong! Every expert was once a beginner.",
            eLearning: "💻 E-Learning",
            vPlatform: "🌐 Virtual Platforms",
            welcome: "Hi! I'm your assistant. How can I help you today?"
        },
        tr: {
            sendPlaceholder: "Sorunuzu yazın...",
            toastProfessor: "Şu anda Profesör modundasınız.",
            toastDean: "Şu anda Dekan modundasınız.",
            toastStudent: "Şu anda Öğrenci modundasınız.",
            toastEmpty: "Lütfen tüm alanları doldurun.",
            overlayProfessor: "Profesör Modu Aktif",
            overlayDean: "Dekan Modu Aktif",
            overlayStudent: "Öğrenci Modu: Hoş geldiniz!",
            schedule: "📅 Haftalık Ders Programı:\nPzt - Matematik 10:00\nSal - Fizik 12:00\nÇar - Yapay Zeka 09:00\nCum - Edebiyat 11:00",
            motivation: "🌟 Güçlü kal! Her uzman bir zamanlar başlayandı.",
            eLearning: "💻 E-Öğrenme",
            vPlatform: "🌐 Sanal Platformlar",
            welcome: "Merhaba! Size nasıl yardımcı olabilirim?"
        },
        pl: {
            sendPlaceholder: "Wpisz swoje pytanie...",
            toastProfessor: "Jesteś teraz w trybie Profesora.",
            toastDean: "Jesteś teraz w trybie Dziekana.",
            toastStudent: "Jesteś teraz w trybie Studenta.",
            toastEmpty: "Proszę wypełnić wszystkie pola.",
            overlayProfessor: "Tryb Profesora Aktywny",
            overlayDean: "Tryb Dziekana Aktywny",
            overlayStudent: "Tryb Studenta: Witamy!",
            schedule: "📅 Plan tygodnia:\nPon - Matematyka 10:00\nWt - Fizyka 12:00\nŚr - AI 09:00\nPt - Literatura 11:00",
            motivation: "🌟 Trzymaj się! Każdy ekspert był kiedyś początkującym.",
            eLearning: "💻 E-Learning",
            vPlatform: "🌐 Wirtualne Platformy",
            welcome: "Cześć! Jak mogę Ci pomóc?"
        }
    };

    const t = key => translations[lang][key] || key;

    function updateLanguageUI() {
        userInput.placeholder = t('sendPlaceholder');
        chatBox.innerHTML = '';
        const quickLinks = document.createElement('div');
        quickLinks.className = 'quick-links';
        quickLinks.innerHTML = `
            <button onclick="window.open('https://uczelnia.akademiata.pl/student/e-learning/')">${t('eLearning')}</button>
            <button onclick="window.open('https://uczelnia.akademiata.pl/student/wirtualne-platformy/')">${t('vPlatform')}</button>
        `;
        chatBox.appendChild(quickLinks);
        addMessage(t('welcome'));
    }

    function addMessage(text, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = isUser ? 'user-message' : 'bot-message';
        messageDiv.textContent = text;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function showToast(message) {
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.textContent = message;
        document.body.appendChild(toast);
        setTimeout(() => toast.classList.add('show'), 100);
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 500);
        }, 3000);
    }

    function showModeOverlay(text) {
        const overlay = document.createElement('div');
        overlay.className = 'mode-overlay';
        overlay.textContent = text;
        document.body.appendChild(overlay);
        setTimeout(() => overlay.classList.add('show'), 50);
        setTimeout(() => overlay.classList.remove('show'), 2000);
        setTimeout(() => overlay.remove(), 2500);
    }

    function changeMode(mode) {
        currentMode = mode;
        const header = document.querySelector('.chat-header');

        const themes = {
            professor: {
                bg: "#e3f2fd",
                header: "#1565c0",
                userBg: "#42a5f5",
                toast: "toastProfessor",
                overlay: "overlayProfessor"
            },
            dean: {
                bg: "#fffde7",
                header: "#fbc02d",
                userBg: "#fff176",
                toast: "toastDean",
                overlay: "overlayDean"
            },
            student: {
                bg: "#e8f5e9",
                header: "#43a047",
                userBg: "#81c784",
                toast: "toastStudent",
                overlay: "overlayStudent"
            },
            default: {
                bg: "#fffdf8",
                header: "#ff6f00",
                userBg: "#ff9800"
            }
        };

        const theme = themes[mode] || themes.default;

        chatContainer.style.backgroundColor = theme.bg;
        header.style.backgroundColor = theme.header;
        document.documentElement.style.setProperty('--primary', theme.header);
        document.documentElement.style.setProperty('--user-bg', theme.userBg);

        if (theme.toast) showToast(t(theme.toast));
        if (theme.overlay) showModeOverlay(t(theme.overlay));

        if (mode === "student") {
            addMessage(t("schedule"));
            addMessage(t("motivation"));
        }

        announcementPopup.classList.toggle('hidden', mode !== "professor" && mode !== "dean");
        exitButton.classList.toggle('hidden', mode === "");
    }

    sendButton.addEventListener('click', () => {
        const question = userInput.value.trim();
        if (!question) return;
        addMessage(question, true);
        userInput.value = '';

        fetch("http://localhost:8000/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question })
        })
            .then(res => res.json())
            .then(data => {
                if (data.mode) {
                    changeMode(data.mode);
                    if (data.message) addMessage(data.message);
                } else {
                    addMessage(data.answer || data.error || "No response");
                }
            })
            .catch(err => {
                console.error("Fetch error:", err);
                addMessage("⚠️ Error reaching the server.");
            });
    });

    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendButton.click();
    });

    languageSelect.addEventListener('change', (e) => {
        lang = e.target.value;
        updateLanguageUI();
    });

    announcementIcon.addEventListener('click', () => {
        announcementPanel.classList.toggle('hidden');
    });

    closePopup.addEventListener('click', () => {
        announcementPopup.classList.add('hidden');
    });

    popupPublish.addEventListener('click', () => {
        const title = popupTitle.value.trim();
        const content = popupContent.value.trim();
        if (!title || !content) return showToast(t("toastEmpty"));

        const announcementText = `📢 ${title}\n${content}`;
        const listItem = document.createElement('li');
        listItem.textContent = announcementText;
        announcementsList.appendChild(listItem);
        addMessage(announcementText);

        popupTitle.value = '';
        popupContent.value = '';
        announcementPopup.classList.add('hidden');
    });

    exitButton.addEventListener('click', () => changeMode(""));

    window.toggleChatBox = () => {
        const chatWrapper = document.getElementById("chatWrapper");
        chatWrapper?.classList.toggle("hidden");
    };

    updateLanguageUI();
});
