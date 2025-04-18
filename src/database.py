import asyncpg
import logging
from datetime import datetime
from src.config import DATABASE_URL

logger = logging.getLogger(__name__)


class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        """Установка соединения с базой данных"""
        try:
            self.pool = await asyncpg.create_pool(DATABASE_URL)

            async with self.pool.acquire() as conn:
                await conn.execute('''
                    CREATE TABLE IF NOT EXISTS user_interactions (
                        id SERIAL PRIMARY KEY,
                        user_id BIGINT NOT NULL,
                        username TEXT,
                        request_text TEXT NOT NULL,
                        response_text TEXT NOT NULL,
                        timestamp TIMESTAMP NOT NULL
                    )
                ''')
            return True
        except Exception as e:
            logger.error(f"Ошибка подключения к базе данных: {e}")
            return False

    async def save_interaction(self, user_id, username, request_text, response_text):
        """Сохранение взаимодействия пользователя в базу данных"""
        if not self.pool:
            logger.warning("Попытка сохранения без подключения к БД")
            return False

        try:
            async with self.pool.acquire() as conn:
                await conn.execute(
                    '''
                    INSERT INTO user_interactions (user_id, username, request_text, response_text, timestamp)
                    VALUES ($1, $2, $3, $4, $5)
                    ''',
                    user_id, username, request_text, response_text, datetime.now()
                )
            return True
        except Exception as e:
            logger.error(f"Ошибка при сохранении взаимодействия: {e}")
            return False

    async def get_user_history(self, user_id, limit=5):
        """Получение истории взаимодействий пользователя"""
        if not self.pool:
            logger.warning("Попытка получения истории без подключения к БД")
            return []

        try:
            async with self.pool.acquire() as conn:
                records = await conn.fetch(
                    '''
                    SELECT request_text, response_text, timestamp 
                    FROM user_interactions 
                    WHERE user_id = $1 
                    ORDER BY timestamp DESC 
                    LIMIT $2
                    ''',
                    user_id, limit
                )
                return records
        except Exception as e:
            logger.error(f"Ошибка при получении истории пользователя: {e}")
            return []

    async def close(self):
        """Закрытие соединения с базой данных"""
        if self.pool:
            await self.pool.close()
