# dependencies
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv
import telebot, time, os

# dotenv
load_dotenv()

#Tokens
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
TOKEN = os.getenv('TOKEN')


bot = telebot.TeleBot(token=TOKEN, parse_mode="markdown")

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

@bot.message_handler(commands=['start'])
def message_handler(message):
    bot.send_message(message.chat.id, "👋 *Hi, I am Frank.* \n \n🌤 I can send the current weather in your locality. \n🐸 I can send memes ;) \n\n🎲 Maybe throw a dice? - /roll \n\n*Developers*\n@PythonNotFound\n@shaunc276", reply_markup=gen_markup())

@bot.message_handler(commands=['help'])
def message_handler(msg):
    bot.send_message(msg.chat.id, "Help", reply_markup=help_markup())

# Sends a dice
@bot.message_handler(commands=['roll'])
def send(msg):
    bot.send_dice(chat_id=msg.chat.id)

# Weather and memes query handler
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "weather":
        bot.send_message(call.message.chat.id, "Send the location.")

        @bot.message_handler(content_types=['location'])
        def handle_location(message):
            # use the openweatherapi here
            print("{0}, {1}".format(message.location.latitude, message.location.longitude))

    elif call.data == "memes":
        bot.send_message(call.message.chat.id, "Memes not added yet :P")


# Polling section
while True:
    try:
        bot.polling()
    
    except Exception:
        print("Failed, Retrying in 15 seconds")
        time.sleep(15)

    