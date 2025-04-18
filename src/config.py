import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot токен
BOT_TOKEN = os.getenv("BOT_TOKEN")

# PostgreSQL настройки
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "telegram_bot")
# Используем localhost для локальной разработки, db для Docker
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

# API ключ для OpenWeatherMap
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Строка подключения к базе данных
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
