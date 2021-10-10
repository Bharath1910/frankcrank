import telebot
import time
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

token = "<API KEY>"

bot = telebot.TeleBot(token=token)

def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2

    markup.add(
        InlineKeyboardButton("Weather", callback_data="cb_yes"),
        InlineKeyboardButton("Memes", callback_data="cb_no")
        )

    return markup

@bot.message_handler(commands=['start'])
def message_handler(message):
    bot.send_message(message.chat.id, "Welcome!", reply_markup=gen_markup())




@bot.message_handler(commands=['roll'])
def send(msg):
    bot.send_dice(chat_id=msg.chat.id)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cb_yes":
        bot.answer_callback_query(call.id, "Weather functions not added yet :P")
    elif call.data == "cb_no":
        bot.answer_callback_query(call.id, "Memes not added yet :P")

@bot.message_handler(content_types=['location'])
def handle_location(message):
    print("{0}, {1}".format(message.location.latitude, message.location.longitude))


while True:
    try:
        bot.polling()
    
    except Exception:
        time.sleep(15)

    