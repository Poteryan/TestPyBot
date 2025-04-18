# Телеграм-бот погоды

Телеграм-бот, который предоставляет информацию о погоде в указанном городе и сохраняет историю взаимодействий пользователя в базе данных PostgreSQL.

## Функциональность

- Получение текущей погоды по названию города через API OpenWeatherMap
- Сохранение истории запросов погоды пользователя в базе данных
- Просмотр истории запросов
- Обработка команд бота (/start, /help, /history)

## Команды бота

- `/start` - Начать взаимодействие с ботом
- `/help` - Показать список доступных команд
- `/history` - Показать историю запросов погоды пользователя (последние 5)

## Технический стек

- Python 3.12
- aiogram - библиотека для создания Telegram ботов
- asyncpg - асинхронный драйвер для PostgreSQL
- aiohttp - асинхронный HTTP клиент для работы с API
- PostgreSQL - база данных для хранения истории запросов
- Docker и Docker Compose для контейнеризации


## Структура базы данных

База данных PostgreSQL содержит одну таблицу `user_interactions` со следующими полями:

- `id` - Уникальный идентификатор записи (SERIAL PRIMARY KEY)
- `user_id` - ID пользователя Telegram (BIGINT)
- `username` - Имя пользователя Telegram (TEXT)
- `request_text` - Текст запроса пользователя (название города) (TEXT)
- `response_text` - Текст ответа бота (данные о погоде) (TEXT)
- `timestamp` - Время взаимодействия (TIMESTAMP)

## Настройка и запуск

### Предварительные требования

- Docker и Docker Compose
- Токен Telegram бота (получить у [@BotFather](https://t.me/BotFather))
- API ключ [OpenWeatherMap](https://openweathermap.org/api)

### Настройка переменных окружения

1. Создайте файл `.env` в корневой директории проекта
2. Заполните его следующими данными:

```
BOT_TOKEN=your_telegram_bot_token
POSTGRES_USER=[USERNAME]
POSTGRES_PASSWORD=[PASSWORD]
POSTGRES_DB=telegram_bot
POSTGRES_HOST=db
POSTGRES_PORT=5432
WEATHER_API_KEY=your_openweathermap_api_key
```

### Запуск с помощью Docker Compose

1. Соберите и запустите контейнеры:

```bash
     docker-compose up -d
```

2. Для просмотра логов:

```bash
  docker-compose logs -f
```

3. Для остановки:

```bash
  docker-compose down
```

## Локальная разработка

### Настройка для локальной разработки

1. Создайте виртуальное окружение:

```bash
    python -m venv venv
    source venv/bin/activate  # для Linux/Mac
    venv\Scripts\activate     # для Windows
```

2. Установите зависимости:

```bash
    pip install -r requirements.txt
```

3. Настройте локальную базу данных PostgreSQL:
   - Установите PostgreSQL на ваш компьютер
   - Создайте базу данных `telegram_bot`
   - Обновите файл `.env`, указав `POSTGRES_HOST=localhost`

4. Запустите бота:

```bash
    python -m src.bot
```



