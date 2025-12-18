# jubber/config.py
""" 
Файл налаштування config.py містить: 
 - токен бота 
"""

from os import environ as env

from dotenv import load_dotenv


load_dotenv()

TOKEN = env['TOKEN']

PRIVATBANK_API_URL = env.get('PRIVATBANK_API_URL', 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5')

HOROSCOPE_API_BASE_URL = env.get('HOROSCOPE_API_BASE_URL', 'https://horoscope-app-api.vercel.app/api/v1/get-horoscope')