Конечно, вот весь `README.md` **в одном куске**, без рамок и без лишнего форматирования — просто скопируй и вставь в файл:

```markdown
# Урок PE4_3 — Бот для озвучки текста с помощью ElevenLabs

Этот проект создан в рамках курса **Zerocoder Promt Engineering 2.0**.

## 🧠 Суть задания

Создать Telegram-бота, который:
- принимает текстовые сообщения от пользователя,
- отправляет текст на озвучку через **API ElevenLabs**,
- возвращает голосовое сообщение в чат.

## ⚙️ Используемые технологии

- Python 3.11+
- Библиотека [`telebot`](https://github.com/eternnoir/pyTelegramBotAPI)
- API [ElevenLabs](https://www.elevenlabs.io/)
- `requests`, `os`, `dotenv`

## 📁 Структура

```
PE4_3/
├── tts_voice_bot.py       # Основной код Telegram-бота
├── .env                   # Переменные окружения (API-ключи)
├── requirements.txt       # Зависимости проекта
└── README.md              # Описание проекта
```

## 🔐 Переменные окружения

Создай `.env` файл в корне с содержимым:

```env
BOT_TOKEN=твой_токен_бота
ELEVENLABS_API_KEY=твой_API_ключ_ElevenLabs
VOICE_ID=идентификатор_голоса
```

## 🚀 Запуск

```bash
pip install -r requirements.txt
python tts_voice_bot.py
```

## ✅ Статус

✔️ Бот работает  
🛠️ Возможны улучшения: выбор голоса, автосоздание `.env`, логирование


```
