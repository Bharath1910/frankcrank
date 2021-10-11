import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv

import time
import os
import requests

load_dotenv()

TOKEN = os.getenv('TOKEN')
WEATHER_API_KEY=os.getenv('WEATHER_API_KEY')
REDDIT_API_KEY=os.getenv('REDDIT_API_KEY')

bot = telebot.TeleBot(token=TOKEN)


@bot.message_handler(commands=['roll'])
def send(msg):
    bot.send_dice(chat_id=msg.chat.id)   


def get_weather(WEATHER_API_KEY, latitude, longitude):
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={WEATHER_API_KEY}'
    result = requests.get(url).json()
    temperature = result['main']['temp']
    # Converting to F
    temperature = round((temperature * 1.8)-459.67)

    feels_like = result['main']['feels_like']
    # Converting to F
    feels_like = round((feels_like * 1.8)-459.67)

    humidity = result['main']['humidity']

    final = {
        "temp": temperature,
        "feels_like": feels_like,
        "humidity": humidity
    }
    return final



@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "How may I help you?\n1. /weather\n2. /memes")


@bot.message_handler(commands=['weather'])
def send_welcome(message):
	bot.reply_to(message, "Send a location to check weather.")



@bot.message_handler(content_types=['location'])
def handle_location(message):
    latitude = message.location.latitude
    longitude = message.location.longitude

    weather_result=get_weather(WEATHER_API_KEY, latitude, longitude)
    final = f"""
                "temp": {weather_result['temp']},
                "feels_like": {weather_result['feels_like']},
                "humidity": {weather_result['humidity']}
            """
    bot.send_message(message.chat.id, final)

    
try:
    bot.infinity_polling()
except Exception:
    time.sleep(15)