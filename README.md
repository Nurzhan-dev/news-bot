# 🤖 Telegram Tesseract OCR Bot

Этот Telegram-бот принимает файлы (PDF, DOCX, изображения), извлекает текст (в том числе на казахском языке 🇰🇿) и публикует его как пост. Также бот прикладывает извлечённые изображения к посту.

---

## 📦 Возможности

- 🧠 OCR на казахском, русском и английском языках (`pytesseract`)
- 📄 Обработка PDF и DOCX файлов (текст + изображения)
- 🖼️ Обработка JPG, PNG изображений
- 📝 Генерация Telegram-постов (заголовок, описание, хэштеги)
- 🐳 Поддержка запуска через Docker и Render

---

## 📁 Структура проекта

├── bot.py # Основной код бота
├── requirements.txt # Python-зависимости
├── Dockerfile # Инструкция для сборки контейнера
├── render.yaml # Конфигурация для деплоя на Render
└── README.md # Документация проекта

---

## 🚀 Запуск (локально)

1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
sudo apt install tesseract-ocr tesseract-ocr-kaz libtesseract-dev poppler-utils
export TELEGRAM_TOKEN=your_token_here
python bot.py
docker build -t telegram-ocr-bot .
docker run -e TELEGRAM_TOKEN=your_token_here telegram-ocr-bot
