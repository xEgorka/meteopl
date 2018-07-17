#!/usr/bin python3

from telegram.ext import Updater
import datetime
from urllib.request import Request, urlopen
from bs4 import  BeautifulSoup
import logging
from telegram.ext import CommandHandler


updater = Updater(token='TOKEN')
dispatcher = updater.dispatcher


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="To get a weather forecast send me required location or use /konigsberg shortcut to see a picture for Kaliningrad.")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


def konigsberg(bot, update):
    q = Request("http://m.meteo.pl/search/eu?miastoEU=&wspolrzedneEU=N54%C2%B041%27+E20%C2%B029%27&typeEU=coords&prognozaEU=60&slugEU=")
    mybytes = urlopen(q).read()
    mystr = mybytes.decode("utf8")
    urlopen(q).close()
    soup = BeautifulSoup(mystr, "html.parser")
    url = soup.find('img', class_='border')['src']
    url = url.replace('=pl','=en')    
    bot.send_photo(chat_id=update.message.chat_id, photo=url)


konigsberg_handler = CommandHandler('konigsberg', konigsberg)
dispatcher.add_handler(konigsberg_handler)


def location(bot, update):
    lat = update.message.location.latitude
    lon = update.message.location.longitude
    lat_deg = str(int(lat))
    lat_min = str(round((int((lat % 1)*60)),2))
    lon_deg = str(int(lon))
    lon_min = str(round((int((lon % 1)*60)),2))
    q = Request("http://m.meteo.pl/search/eu?miastoEU=&wspolrzedneEU=N"+ lat_deg +"%C2%B0"+ lat_min +"%27+E"+ lon_deg +"%C2%B0"+ lon_min +"%27&typeEU=coords&prognozaEU=60&slugEU=")
    mybytes = urlopen(q).read()
    mystr = mybytes.decode("utf8")
    urlopen(q).close()
    soup = BeautifulSoup(mystr, "html.parser")
    url = soup.find('img', class_='border')['src']
    url = url.replace('=pl','=en')	
    bot.send_photo(chat_id=update.message.chat_id, photo=url)

from telegram.ext import MessageHandler, Filters
location_handler = MessageHandler(Filters.location, location)
dispatcher.add_handler(location_handler)
	
updater.start_polling()