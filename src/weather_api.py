import aiohttp
from src.config import WEATHER_API_KEY


class WeatherAPI:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    @staticmethod
    async def get_weather(city):
        """Получение данных о погоде для указанного города"""
        params = {
            'q': city,
            'appid': WEATHER_API_KEY,
            'units': 'metric',
            'lang': 'ru'
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(WeatherAPI.BASE_URL, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return WeatherAPI._format_weather_data(data)
                else:
                    error_data = await response.json()
                    return f"Ошибка: {error_data.get('message', 'Неизвестная ошибка')}"

    @staticmethod
    def _format_weather_data(data):
        """Форматирование данных о погоде для отображения пользователю"""
        city_name = data['name']
        country = data['sys']['country']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        description = data['weather'][0]['description']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        return (
            f"🌍 Погода в {city_name}, {country}:\n"
            f"🌡️ Температура: {temp}°C (ощущается как {feels_like}°C)\n"
            f"☁️ Состояние: {description}\n"
            f"💧 Влажность: {humidity}%\n"
            f"💨 Скорость ветра: {wind_speed} м/с"
        )
