# 🎮 Steam Analytic
___
## 📝 Опис
**Steam Analytic** — це **REST API** для збору, обробки та аналізу даних зі Steam. API дозволяє: 
- 📊 Отримувати аналітику ігор, категорій, знижок, мов тощо.
- 🎯 Проводити фільтрацію за параметрами
- 👤 Працювати з користувачами (авторизація, облікові записи)
- 🔄 Оновлювати дані зі Steam API
- 👥 Отримувати інформацію про гравців та порівнювати їх

---

## 🧰 Технології
![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-async-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![Docker](https://img.shields.io/badge/Docker-ready-blue)
![Celery](https://img.shields.io/badge/Celery-background_tasks-yellowgreen)
![Redis](https://img.shields.io/badge/Redis-broker-red)
![Alembic](https://img.shields.io/badge/Alembic-migrations-important)
![Swagger](https://img.shields.io/badge/Docs-Swagger_UI-orange)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)

---

## 📦 Структура проєкту
___
## Структура проєкту
```
steam-analytic/
│
├── app/                         # Основна логіка програми
│   ├── api/                     # FastAPI роутери та точки входу для API
│   ├── application/             # Конфігурації, залежності, запуск Celery тощо
│   ├── certs/                   # SQLAlchemy-моделі, сесії БД, Alembic
│   ├── domain/                  # Бізнес-логіка: інтеграція зі Steam API, Telegram-бот
│   ├── infrastructure/          # Celery-задачі та взаємодія з Redis / брокерами
│   ├── utils/                   # Pydantic-схеми, утилітарні функції
│   └── main.py                  # Точка входу: запуск FastAPI
│
├── tests/                       # Тести для всіх рівнів логіки
├── alembic/                     # Міграції бази даних (Alembic)
├── Dockerfile                   # Контейнеризація застосунку
├── docker-compose.yml           # Сервіси: API, PostgreSQL, Redis, Celery
├── requirements.txt             # Залежності проєкту
├── .env                         # Секрети та налаштування середовища
├── LICENSE                      # Ліцензія MIT
└── README.md                    # Документація
```
---
# Запуск
## 1 Клонування
```shell

git clone https://github.com/floyse-back/SteamAnalitic.git
```
## 2 Підготовка до запуску
```shell

pip install -r requirements.txt
alembic upgrade head
```
#### :exclamation: Переконайтесь, що `.env` створений на основі `.env.example`
#### Також створіть в app папку certs `app/certs` та в цій папці згенеруйте `public key` та `private key`
### 🔐 Генерація ключів
```shell
cd app/certs
openssl genrsa -out jwt-private.pem
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
```
## 3 Запуск системи
### Fast API
```shell

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
### Celery
```shell

celery -A app.infrastructure.celery_worker.celery worker --loglevel=info
```
## 🐳 Docker запуск (альтернатива)
```shell

docker compose up --build
```
___
## Документація 
#### Swagger доступний за адресою:
http://localhost:8000/docs
___
## 🧪 Тестування системи
```
pytest
```
---
## 👨‍💻 Автор
### [floyse-back](https://github.com/floyse-back) — розробка, проєктування та документація.