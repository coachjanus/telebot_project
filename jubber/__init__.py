# jubber/__init__.py

from zoneinfo import ZoneInfo
import datetime

__app_name__ = "jubber"


# GREETINGS = '''
#   Hawaii! 
#   Get daily horoscope for your zodiac sign.
#     - To get daily horoscope press /horoscope

# '''

HOROSCOPE = '''What's your zodiac sign?\nChoose one: *Aries*, *Taurus*, *Gemini*, *Cancer,* *Leo*, *Virgo*, *Libra*, *Scorpio*, *Sagittarius*, *Capricorn*, *Aquarius*, and *Pisces*'''

GREETINGS = '''
  Hawaii! 
  Get daily horoscope for your zodiac sign.
    - To get daily horoscope press /horoscope
  I can show you PrivatBank exchange rates.
    - To get the exchange rates press /exchange.
    - To get help press /help.
'''

HELP_MESSAGES = '''
 1) To receive a list of available currencies press /exchange.
 2) Click on the currency you are interested in.
 3) You will receive a message containing information regarding the source and the target currencies, buying rates and selling rates.
 4) Click “Update” to receive the current information regarding the request. The bot will also show the difference between the previous and the current exchange rates.
 5) The bot supports inline. Type @<botusername> in any chat and the first letters of a currency.
'''

EMOJI_UP = u"\U0001F4C8"  # 📈
EMOJI_DOWN = u"\U0001F4C9"  # 📉

""" 
 Часовий пояс потрібен, щоб вказати час оновлення повідомлення. 
 Telegram API не дозволяє дізнатися часовий пояс користувача,тому 
 оновлений час має відображатися з підказкою про часовий пояс.
"""

TIMEZONE = 'Europe/Kiev'
TIMEZONE_COMMON_NAME = 'Kiev'

P_TIMEZONE = ZoneInfo(TIMEZONE)

def get_edited_signature():
    return f'''<i>Updated {datetime.datetime.now(P_TIMEZONE).strftime('%H:%M:%S')} ({TIMEZONE})</i>'''
