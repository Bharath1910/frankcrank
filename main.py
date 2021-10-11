import telebot
import time
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

token = "2062019393:AAFPC4C-O9QwNa1MSMowZVWKpTTeh9J2KQk"

bot = telebot.TeleBot(token=token)

def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2

    markup.add(
        InlineKeyboardButton("Weather", callback_data="weather"),
        InlineKeyboardButton("Memes", callback_data="memes")
        )

    return markup

@bot.message_handler(commands=['start'])
def message_handler(message):
    bot.send_message(message.chat.id, "Welcome!", reply_markup=gen_markup())

@bot.message_handler(commands=['roll'])
def send(msg):
    bot.send_dice(chat_id=msg.chat.id)

@bot.message_handler(content_types=['location'])
def handle_location(message):
    print("{0}, {1}".format(message.location.latitude, message.location.longitude))

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "weather":
        bot.send_message(call.message.chat.id, "Send the location.")

        @bot.message_handler(content_types=['location'])
        def handle_location(message):
            print("{0}, {1}".format(message.location.latitude, message.location.longitude))

    elif call.data == "memes":
        bot.send_message(call.message.chat.id, "Memes not added yet :P")


while True:
    try:
        bot.polling()
    
    except Exception:
        time.sleep(15)

    