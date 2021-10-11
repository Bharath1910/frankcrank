# dependencies
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv
import telebot, time, os, requests

### SAMPLE DATA ###
Sample_data = {
  "coord": {
    "lon": -122.08,
    "lat": 37.39
  },
  "weather": [
    {
      "id": 800,
      "main": "Clear",
      "description": "clear sky",
      "icon": "01d"
    }
  ],
  "base": "stations",
  "main": {
    "temp": 282.55,
    "feels_like": 281.86,
    "temp_min": 280.37,
    "temp_max": 284.26,
    "pressure": 1023,
    "humidity": 100
  },
  "visibility": 16093,
  "wind": {
    "speed": 1.5,
    "deg": 350
  },
  "clouds": {
    "all": 1
  },
  "dt": 1560350645,
  "sys": {
    "type": 1,
    "id": 5122,
    "message": 0.0139,
    "country": "US",
    "sunrise": 1560343627,
    "sunset": 1560396563
  },
  "timezone": -25200,
  "id": 420006353,
  "name": "Mountain View",
  "cod": 200
  }
### SAMPLE DATA ###
# dotenv
load_dotenv()

#Tokens
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
TOKEN = os.getenv('TOKEN')


bot = telebot.TeleBot(token=TOKEN, parse_mode="markdown")

# INLINE KEYBOARD BUTTON LAYOUT, For /start
def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2

    markup.add(
        InlineKeyboardButton("Weather", callback_data="weather"),
        InlineKeyboardButton("Memes", callback_data="memes"),
        InlineKeyboardButton("Check out my source code", url="https://github.com/bharath1910/frankcrank" )
        )

    return markup

# INLINE KEYBOARD BUTTON LAYOUT, For /help
def help_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2

    markup.add(
        InlineKeyboardButton("PythonNotFound", url="https://t.me/pythonnotfound"),
        InlineKeyboardButton("Shaun", url="https://t.me/shaunc276"),
        InlineKeyboardButton("Submit Bugs", url="https://github.com/bharath1910/frankcrank/issues" )
        )

    return markup

# /start
@bot.message_handler(commands=['start'])
def message_handler(message):
    bot.send_message(message.chat.id, "👋 *Hi, I am Frank.* \n \n🌤 I can send the current weather in your locality. \n🐸 I can send memes ;) \n\n🎲 Maybe throw a dice? - /roll \n\n*Developers*\n@PythonNotFound\n@shaunc276", reply_markup=gen_markup())

# /help, sends help text
@bot.message_handler(commands=['help'])
def msg_handler(msg):
    bot.send_message(msg.chat.id,"👋 *Hi, I have 3 main functions.*\n\n *1. ⛅️ Get local weather*\n    - Send /start to me and click the weather button.\n    - Click the 📎 and send the location to get the weather data.\n    - *Note:* This will only works on Mobile.\n\n*2.🐸 Get desired memes!*\n    - This feature is not yet implemented\n\n*3.🎲 Roll em!*\n    - Send /roll to me and I will roll a dice for ya\n\nIf you happened to find any bugs, feel free to message *PythonNotFound* or *Shaun*, or open a new issue on the bot's GitHub Page.\n\n*Made with ❤️ using Python.*", reply_markup=help_markup())

# /roll, Sends a dice
@bot.message_handler(commands=['roll'])
def send(msg):
    bot.send_dice(chat_id=msg.chat.id)

# Weather and memes query handler
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "weather":
        bot.send_message(call.message.chat.id, f"Send the location, /help for more info.")

        @bot.message_handler(content_types=['location'])
        def handle_location(message):
            # use the openweatherapi here
            # Note : this is a sample output from the Sample_data.
            bot.send_message(message.chat.id,f"{Sample_data['weather'][0]['main']}, Expected {Sample_data['weather'][0]['description']} on Mountain View.\n\n*More Information:*\n    *-  Average Temperature* : {Sample_data['main']['temp']}K\n    *-  Minimum Temperature* : {Sample_data['main']['temp_min']}\n    *-  Maximum Temperature* : {Sample_data['main']['temp_max']}\n    *-  Atmospheric Pressure* : {Sample_data['main']['pressure']}\n    *-  Humidity* : {Sample_data['main']['humidity']}%\n\nWind speed *1.5km/h* due *East*\n\n")
            

    elif call.data == "memes":
        # Use PRAW here
        bot.send_message(call.message.chat.id, "Memes not added yet :P")


# Polling section
bot.infinity_polling()

    