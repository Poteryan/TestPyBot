import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

from src.config import BOT_TOKEN
from src.database import Database
from src.weather_api import WeatherAPI

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Инициализация базы данных
db = Database()


@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    await message.answer(
        "👋 Привет! Я бот погоды.\n\n"
        "Отправь мне название города, и я покажу текущую погоду.\n"
        "Используй /help для получения списка команд."
    )
    # Команды не сохраняем в базу данных


@dp.message(Command("help"))
async def cmd_help(message: Message):
    """Обработчик команды /help"""
    help_text = (
        "🔍 Доступные команды:\n\n"
        "/start - Начать взаимодействие с ботом\n"
        "/help - Показать список команд\n"
        "/history - Показать историю ваших запросов (последние 5)\n\n"
        "Чтобы узнать погоду, просто отправьте название города."
    )
    await message.answer(help_text)
    # Команды не сохраняем в базу данных


@dp.message(Command("history"))
async def cmd_history(message: Message):
    """Обработчик команды /history"""
    try:
        history = await db.get_user_history(message.from_user.id)

        if not history:
            response_text = "У вас пока нет истории запросов."
        else:
            response_text = "📜 Ваша история запросов:\n\n"
            for i, record in enumerate(history, 1):
                request = record['request_text']
                timestamp = record['timestamp'].strftime("%d.%m.%Y %H:%M")
                response_text += f"{i}. {timestamp}: {request}\n"

        await message.answer(response_text)
        # Команды не сохраняем в базу данных
    except Exception as e:
        logger.error(f"Ошибка при работе с историей: {e}")
        await message.answer("Произошла ошибка при получении истории. Пожалуйста, попробуйте позже.")


@dp.message()
async def handle_message(message: Message):
    """Обработчик текстовых сообщений"""
    city = message.text.strip()

    # Получаем данные о погоде
    try:
        weather_response = await WeatherAPI.get_weather(city)

        # Отправляем ответ пользователю
        await message.answer(weather_response)

        # Сохраняем взаимодействие в базу данных
        # Только текстовые запросы (города) сохраняем в базу данных
        try:
            await db.save_interaction(
                message.from_user.id,
                message.from_user.username,
                city,
                weather_response
            )
            logger.info(f"Сохранен запрос погоды для города: {city}")
        except Exception as e:
            logger.error(f"Ошибка при сохранении в БД: {e}")
    except Exception as e:
        logger.error(f"Ошибка при получении погоды: {e}")
        await message.answer(
            "Произошла ошибка при получении данных о погоде. Пожалуйста, проверьте название города и попробуйте снова."
        )


async def main():
    """Основная функция запуска бота"""
    # Подключаемся к базе данных
    try:
        await db.connect()
        logger.info("Успешное подключение к базе данных")
    except Exception as e:
        logger.error(f"Ошибка подключения к базе данных: {e}")
        logger.warning("Бот будет работать без сохранения в базу данных")

    # Запускаем бота
    try:
        logger.info("Запуск бота...")
        await dp.start_polling(bot)
    finally:
        if db.pool:
            await db.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
