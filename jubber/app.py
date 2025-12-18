# 

import telebot
import json

import jubber.config as config


from jubber import GREETINGS, HOROSCOPE, HELP_MESSAGES
from jubber.exchange_helpers import get_edited_signature, get_exchange_diff, serialize_ex

from jubber.horoscope_api import get_daily_horoscope, get_monthly_horoscope, get_weekly_horoscope

import jubber.exchange_api as exchange_api

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def welcome(message):
    bot.reply_to(message, GREETINGS)

@bot.message_handler(commands=['horoscope'])
def sign_handler(message):
    sent_msg = bot.send_message(message.chat.id, HOROSCOPE, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, day_handler)

def day_handler(message):
    sign = message.text
    text = (
        "What day do you want to know?\n"
        "Choose one: *TODAY*, *TOMORROW*, *YESTERDAY*, *WEEK* or *MONTH*."
    )
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, fetch_horoscope, sign.capitalize())

VALID_ZODIAC_SIGNS = {
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
}

VALID_DAYS = {"Today", "Tomorrow", "Yesterday", "Week", "Month"}
def is_valid_zodiac_sign(sign):
    return sign.capitalize() in VALID_ZODIAC_SIGNS

def fetch_horoscope(message, sign):
    
    if not is_valid_zodiac_sign(sign):
        bot.send_message(message.chat.id, "Invalid zodiac sign. Please try again!")
        return

    day = message.text.capitalize()
    if day not in VALID_DAYS:
        bot.send_message(message.chat.id, "Invalid day selection. Choose: Today, Tomorrow, Yesterday, Week, or Month.")
        return

    # Fetch the horoscope based on valid input
    # print("challenging_days", day)
    if day == 'Week':
        horoscope = get_weekly_horoscope(sign)
        # print("WEEK", horoscope)
        challenging_days = "week"
    elif day == 'Month':
        horoscope = get_monthly_horoscope(sign)
        challenging_days = "month"
    else:
        horoscope = get_daily_horoscope(sign, day)
        challenging_days = "date"
    
    data = horoscope["data"]
    horoscope_message = f'*Horoscope:* {data["horoscope_data"]}\n*Sign:* {sign}\n*Day:* {data[challenging_days]}'
    bot.send_message(message.chat.id, "Here's your horoscope!")
    bot.send_message(message.chat.id, horoscope_message, parse_mode="Markdown")

@bot.message_handler(commands=['help'])
def send_help(message):
   keyboard = telebot.types.InlineKeyboardMarkup()
   keyboard.add(
       telebot.types.InlineKeyboardButton(
        'Message the developer', url='https://t.me/couchjanus'
       )
   )
   bot.reply_to(message, HELP_MESSAGES, reply_markup=keyboard)

# exchange
@bot.message_handler(commands=['exchange'])
def send_exchange(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    
    keyboard.row(telebot.types.InlineKeyboardButton('USD', callback_data='get-USD'), telebot.types.InlineKeyboardButton('EUR', callback_data='get-EUR'))

    bot.reply_to(message, 'Click on the currency of choice:', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
   data = query.data
   if data.startswith('get-'):
       get_ex_callback(query)

# Let’s implement the get_ex_callback method:

def get_ex_callback(query):
   bot.answer_callback_query(query.id)
   send_exchange_result(query.message, query.data[4:])

def send_exchange_result(message, ex_code):
   bot.send_chat_action(message.chat.id, 'typing')
   ex = exchange_api.get_exchange(ex_code)
   bot.send_message(
       message.chat.id, serialize_ex(ex),
       reply_markup=get_update_keyboard(ex),
       parse_mode='HTML'
   )

def get_update_keyboard(ex):
   keyboard = telebot.types.InlineKeyboardMarkup()
   keyboard.row(
       telebot.types.InlineKeyboardButton(
           'Update',
           callback_data=json.dumps({
               't': 'u',
               'e': {
                   'b': ex['buy'],
                   's': ex['sale'],
                   'c': ex['ccy']
               }
           }).replace(' ', '')
       ),
       telebot.types.InlineKeyboardButton('Share', switch_inline_query=ex['ccy'])
   )
   return keyboard


# Unified callback handler – routes exchange requests and update actions
@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    data = query.data
    # Exchange request (e.g., "get-USD")
    if data.startswith('get-'):
        get_ex_callback(query)
        return
    # Update request – payload is a JSON string with "t":"u"
    try:
        payload = json.loads(data)
        if payload.get('t') == 'u':
            edit_message_callback(query, payload['e'])
    except (ValueError, KeyError):
        # Silently ignore malformed payloads
        pass

def edit_message_callback(query, payload):
    """Refresh exchange data and edit the original message.

    ``payload`` is the ``e`` dict extracted from the callback JSON and contains
    the original ``buy``, ``sale`` and ``c`` (currency) values.
    """
    exchange_now = exchange_api.get_exchange(payload['c'])
    text = (
        serialize_ex(
            exchange_now,
            get_exchange_diff(
                get_ex_from_iq_data(payload),
                exchange_now,
            ),
        )
        + "\n"
        + get_edited_signature()
    )
    if query.message:
        # Explicitly pass ``chat_id`` and ``message_id`` – the previous version
        # relied on positional arguments which could be mis‑interpreted.
        bot.edit_message_text(
            text,
            chat_id=query.message.chat.id,
            message_id=query.message.message_id,
            reply_markup=get_update_keyboard(exchange_now),
            parse_mode='HTML',
        )
    elif getattr(query, "inline_message_id", None):
        bot.edit_message_text(
            text,
            inline_message_id=query.inline_message_id,
            reply_markup=get_update_keyboard(exchange_now),
            parse_mode='HTML',
        )
def get_ex_from_iq_data(exc_json):
   return {
       'buy': exc_json['b'],
       'sale': exc_json['s']
   }

@bot.message_handler(func=lambda message: True)
def unknown_command(message):
    bot.reply_to(message, "Sorry, I didn't understand that command. Type /help for assistance.")

# Two handlers match func=lambda message: True, creating ambiguity:
# Remove the redundant echo_all handler and keep only the unknown_command handler to manage unrecognized commands.
# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
#    bot.reply_to(message, message.text)