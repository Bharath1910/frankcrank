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
# bot = telebot.TeleBot(token=TOKEN, parse_mode="markdown")


@bot.message_handler(commands=['roll'])
def send(msg):
    bot.send_dice(chat_id=msg.chat.id)   


def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2

    markup.add(
        InlineKeyboardButton("Weather", callback_data="weather"),
        InlineKeyboardButton("Memes", callback_data="memes"),
        InlineKeyboardButton("Check out my source code", url="https://github.com/bharath1910/frankcrank" )
        )

    return markup

def help_markup():
    markup1 = InlineKeyboardMarkup()
    markup1.row_width(2)

    markup1.add(
        InlineKeyboardButton("Contact", url="https://t.me/PythonNotFound"),
        InlineKeyboardButton("Contact",url="https://t.me/shaunc276" ),
        InlineKeyboardButton("Submit New Issue on GitHub", url="https://github.com/Bharath1910/frankcrank/issues")
    )
    
    return markup1


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
    weather = result['weather'][0]['main']
    final = {
        "weather": weather,
        "temp": temperature,
        "feels_like": feels_like,
        "humidity": humidity
    }
    return final



@bot.message_handler(commands=['start'])
def message_handler(message):
    bot.send_message(message.chat.id, "👋 *Hi, I am Frank.* \n \n🌤 I can send the current weather in your locality. \n🐸 I can send memes ;) \n\n🎲 Maybe throw a dice? - /roll \n\n*Developers*\n@PythonNotFound\n@shaunc276", reply_markup=gen_markup())

@bot.message_handler(commands=['help'])
def message_handler(msg):
    bot.send_message(msg.chat.id, "Help", reply_markup=help_markup())


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "weather":
        bot.send_message(call.message.chat.id, "Send the location.")

        @bot.message_handler(content_types=['location'])
        def handle_location(message):
            latitude = message.location.latitude
            longitude = message.location.longitude

            weather_result=get_weather(WEATHER_API_KEY, latitude, longitude)
    
            final = (
                f"""
                    weather: {weather_result['weather']}
                    temperature: {weather_result['temp']},
                    feels_like: {weather_result['feels_like']},
                    humidity: {weather_result['humidity']}
                """)
            bot.send_message(message.chat.id, final)

    elif call.data == "memes":
        bot.send_message(call.message.chat.id, "Memes not added yet :P")
        


bot.infinity_polling()