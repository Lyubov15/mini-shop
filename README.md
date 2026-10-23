# Mini App Shop (MVP)

Минимальный рабочий прототип интернет-магазина. Проект включает в себя Telegram-бота для администрирования товаров и Telegram Mini App (веб-каталог) для их просмотра.

## Стек технологий
*   **Frontend:** Next.js 15+ (App Router), React
*   **Backend:** FastAPI (Python 3.13), SQLAlchemy (async)
*   **Telegram Bot:** Aiogram 3.x
*   **База данных:** PostgreSQL 16
*   **S3 Хранилище:** MinIO
*   **Инфраструктура:** Docker Compose, Ngrok

## Функционал
1.  **Бот (Aiogram):**
    *   Команда `/start` с кнопкой открытия Telegram Mini App.
    *   Добавление товара администратором (отправка фото с подписью в одном сообщении).
    *   Загрузка фото в MinIO и сохранение записи в PostgreSQL.
2.  **Каталог (Next.js):**
    *   Отображение списка товаров с фотографиями.
    *   Удаление товаров (через прокси-роуты Next.js).
    *   Работает как в обычном браузере, так и внутри Telegram.
3.  **Бэкенд (FastAPI):**
    *   Асинхронная работа с PostgreSQL.
    *   Стриминг изображений из MinIO.
    *   Настроен CORS для работы с фронтендом.

## Инструкция по локальному запуску

**1. Требования**

Для запуска проекта необходимы:

- Docker и Docker Desktop
- Python 3.12+
- Node.js 18+
- Аккаунт Ngrok (для HTTPS-ссылки для Telegram Mini App)

**2. Настройка окружения**

Создайте файл `.env` в корне проекта и добавьте туда токен вашего Telegram-бота:

```env
TELEGRAM_BOT_TOKEN=ваш_токен_от_BotFather
```

**3. Запуск инфраструктуры (БД и MinIO)**

В корне проекта выполните:

```bash
docker compose up -d
```

В MinIO (панель управления `http://localhost:9001`, логин/пароль: `minioadmin`) нужно вручную создать бакет с названием `basket`.

**4. Запуск Бэкенда (FastAPI)**

Откройте терминал и выполните:

```bash
cd backend
python -m venv venv
```

**Windows:**

```bash
venv\Scripts\activate
```

**Mac/Linux:**

```bash
source venv/bin/activate
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

Запустите сервер:

```bash
uvicorn main:app --reload
```

API доступно по адресу `http://localhost:8000`.

**5. Запуск Фронтенда (Next.js)**

Откройте новый терминал:

```bash
cd frontend
npm install
npm run dev -- -H 0.0.0.0
```

Сайт доступен по адресу `http://localhost:3000`.

**6. Запуск Бота (Aiogram)**

Откройте новый терминал:

```bash
cd bot
python -m venv venv
```

**Windows:**

```bash
venv\Scripts\activate
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

Запустите бота:

```bash
python bot.py
```
