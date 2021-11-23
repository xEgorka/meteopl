#!/usr/bin python3
import datetime
import logging

from bs4 import BeautifulSoup
from random import randrange
from urllib.request import Request, urlopen

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters


#nohup python3 main.py &
updater = Updater(token=
    '',
    use_context=True
)
dispatcher = updater.dispatcher
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
text = (
    """Share some location to get a weather picture or send /Konigsberg
    command to see the picture for Kaliningrad.\nHow to read forecast: /legend"""
)


def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=text)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


def konigsberg(update, context):
    q = Request("http://m.meteo.pl/row/339/col/241")
    mybytes = urlopen(q).read()
    mystr = mybytes.decode("utf8")
    urlopen(q).close()
    soup = BeautifulSoup(mystr, "html.parser")
    url = soup.find('img', class_='border')['src']
    url = url.replace('=pl','=en')
    print(f'chat_id = {update.message.chat_id}')
    context.bot.send_photo(chat_id=update.message.chat_id, photo=url)
    if randrange(10) == 0:
        context.bot.send_message(
            chat_id=update.message.chat_id, text=(
                """Try to share any location
                to get forecast for that place! 📍"""
            )
        )


konigsberg_handler = CommandHandler('konigsberg', konigsberg)
dispatcher.add_handler(konigsberg_handler)

def location(update, context):
    lat = update.message.location.latitude
    lon = update.message.location.longitude
    url = (
        "http://www.meteo.pl/um/php/mgram_search.php?NALL=" + str(lat) +
        "&EALL=" + str(lon) + "&lang=en"
    )
    q = urlopen(url)
    finalurl = q.geturl()
    #print(finalurl)
    row = finalurl[finalurl.index('&row=') + 5:finalurl.index('&col=')]
    col = finalurl[finalurl.index('&col=') + 5:finalurl.index('&lang')]
    lat_deg = str(int(lat))
    lat_min = str(round((int((lat % 1)*60)),2))
    lon_deg = str(int(lon))
    lon_min = str(round((int((lon % 1)*60)),2))
    q = Request("http://m.meteo.pl/row/" + str(row) + "/col/" + str(col))
    mybytes = urlopen(q).read()
    mystr = mybytes.decode("utf8")
    urlopen(q).close()
    soup = BeautifulSoup(mystr, "html.parser")
    url = soup.find('img', class_='border')['src']
    url = url.replace('=pl','=en')
    print(f'chat_id = {update.message.chat_id}')
    context.bot.send_photo(chat_id=update.message.chat_id, photo=url)


location_handler = MessageHandler(Filters.location, location)
dispatcher.add_handler(location_handler)


def legend(update, context):
    url = "https://www.meteo.pl/um/metco/leg_um_en_cbase_256.png"
    context.bot.send_photo(chat_id=update.message.chat_id, photo=url)


legend_handler = CommandHandler('legend', legend)
dispatcher.add_handler(legend_handler)

updater.start_polling()
