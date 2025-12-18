""" Bot entry point script. jubber/__main__.py"""

from jubber import __app_name__
from jubber.app import bot

# if __name__ == '__main__':
# 	print(f'\nStarted telegram bot {__app_name__}\n')
# 	bot.infinity_polling()

if __name__ == '__main__':
    try:
        print(f'\nStarted telegram bot {__app_name__}\n')
        bot.infinity_polling()
    except Exception as e:
        print(f"Error occurred: {e}")