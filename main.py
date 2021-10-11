import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv


import math
import os
import requests

load_dotenv()


TOKEN = os.getenv('TOKEN')
WEATHER_API_KEY=os.getenv('WEATHER_API_KEY')

bot = telebot.TeleBot(token=TOKEN, parse_mode="markdown")


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
    markup = InlineKeyboardMarkup()
    markup.row_width = 2

    markup.add(
        InlineKeyboardButton("PythonNotFound", url="https://t.me/pythonnotfound"),
        InlineKeyboardButton("Shaun", url="https://t.me/shaunc276"),
        InlineKeyboardButton("Submit Bugs", url="https://github.com/bharath1910/frankcrank/issues" )
        )

    return markup


def get_weather(WEATHER_API_KEY, latitude, longitude):
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={WEATHER_API_KEY}'
    result = requests.get(url).json()


    main = result['weather'][0]['main']
    description = result['weather'][0]['description']
    temp = result['main']['temp']
    temp = math.floor(temp -273.15)
    temp_min = result['main']['temp_min']
    temp_min = math.floor(temp_min -273.15)
    temp_max = result['main']['temp_max']
    temp_max = math.floor(temp_max -273.15)
    pressure = result['main']['pressure']
    humidity = result['main']['humidity']
    windspeed = result['wind']['speed']
    wind_degree = result['wind']['deg']
    final = {
        "main": main,
        "description": description,
        "temp": temp,
        "temp_min": temp_min,
        "temp_max": temp_max,
        "pressure": pressure,
        "humidity": humidity,
        "windspeed": windspeed,
        "wind_degree": wind_degree
    }
    return final



@bot.message_handler(commands=['start'])
def message_handler(message):
    bot.send_message(message.chat.id, "👋 *Hi, I am Frank.* \n \n🌤 I can send the current weather in your locality. \n🐸 I can send memes ;) \n\n🎲 Maybe throw a dice? - /roll \n\n*Developers*\n@PythonNotFound\n@shaunc276", reply_markup=gen_markup())

@bot.message_handler(commands=['help'])
def msg_handler(msg):
    bot.send_message(msg.chat.id,"👋 *Hi, I have 3 main functions.*\n\n *1. ⛅️ Get local weather*\n    - Send /start to me and click the weather button.\n    - Click the 📎 and send the location to get the weather data.\n    - *Note:* This will only works on Mobile.\n\n*2.🐸 Get desired memes!*\n    - This feature is not yet implemented\n\n*3.🎲 Roll em!*\n    - Send /roll to me and I will roll a dice for ya\n\nIf you happened to find any bugs, feel free to message *PythonNotFound* or *Shaun*, or open a new issue on the bot's GitHub Page.\n\n*Made with ❤️ using Python.*", reply_markup=help_markup())



def ms_km(num):
    return (math.floor(3.6 * num))

def degrees_to_direction(deg):
    dir_arr = [
            "North","North-North East",
            "North East","East-North East",
            "East","East South East",
            "South East","South-South East",
            "South","South-South West",
            "South West","West-South West",
            "West","West-North West",
            "North West","North-North West",
            "North"
            ]

    return dir_arr[int(((deg%360)//22.5))]


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "weather":
        bot.send_message(call.message.chat.id, "Send the location.")

        @bot.message_handler(content_types=['location'])
        def handle_location(message):
            latitude = message.location.latitude
            longitude = message.location.longitude

            weather_result=get_weather(WEATHER_API_KEY, latitude, longitude)
            bot.send_message(message.chat.id,f"{weather_result['main']}, Expected {weather_result['description']} on Mountain View.\n\n*More Information:*\n    *-  Average Temperature* : {weather_result['temp']}C\n    *-  Minimum Temperature* : {weather_result['temp_min']}C\n    *-  Maximum Temperature* : {weather_result['temp_max']}C\n    *-  Atmospheric Pressure* : {weather_result['pressure']}hpa\n    *-  Humidity* : {weather_result['humidity']}%\n\nWind speed *{ms_km(weather_result['windspeed'])}km/h* due *{degrees_to_direction(weather_result['wind_degree'])}*\n\n")


    elif call.data == "memes":
        bot.send_message(call.message.chat.id, "Memes not added yet :P")
        


bot.infinity_polling()