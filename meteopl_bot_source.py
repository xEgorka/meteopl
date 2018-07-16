#!/usr/bin python3

from telegram.ext import Updater
import datetime
import pytz

updater = Updater(token='TOKEN')
dispatcher = updater.dispatcher

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def start(bot, update):
    tz = pytz.timezone('Europe/Warsaw')
    now = datetime.datetime.now(tz)
    if now.hour >= 0 and now.hour < 10:
        x = '00'
    elif now.hour >=10 and now.hour < 16:
        x = '06'
    elif now.hour >=16 and now.hour < 22:
        x = '12'
    elif now.hour >=22 and now.hour <= 4:
        x = '18'
    dd = now.strftime("%Y%m%d") + x
    url = 'https://www.meteo.pl/um/metco/mgram_pict.php?ntype=0u&fdate=' + dd + '&row=339&col=241&lang=en'
    bot.send_photo(chat_id=update.message.chat_id, photo=url)

from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()
