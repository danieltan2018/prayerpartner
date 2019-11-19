# pip install schedule

import telegram
from telegram.ext import (Updater)
import logging
import schedule
import time

bottoken = 'x'  # replace with actual bot token
bot = telegram.Bot(token=bottoken)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

message = '''
<b>YF Prayer Partners (1 Jan - 1 Feb)</b>
@example1 & @example3
@example2 & @example4
'''


def job():
    # replace with actual chat id
    bot.send_message(chat_id=1, text=message,
                     parse_mode=telegram.ParseMode.HTML)
    return schedule.CancelJob


def main():
    updater = Updater(
        token=bottoken, use_context=True)

    schedule.every().monday.at("00:00").do(job)

    while True:
        schedule.run_pending()
        time.sleep(25)

    updater.start_polling()


if __name__ == '__main__':
    main()
