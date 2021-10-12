# dependencies
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import telebot, requests, math, os, time, praw, random
from dotenv import load_dotenv
load_dotenv()

# secrets
TOKEN = os.getenv('TOKEN')
WEATHER_API_KEY=os.getenv('WEATHER_API_KEY')

# PRAW setup
reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    username=os.getenv('REDDIT_USERNAME'),
    password=os.getenv('REDDIT_PASSWORD'),
    user_agent="Frank"
)

# Telebot setup
bot = telebot.TeleBot(
    token=TOKEN, 
    parse_mode="markdown"
    )


def help_markup():
    """
    Inline keyboard button layout, for /help
    """

    markup = InlineKeyboardMarkup()
    markup.row_width = 2

    markup.add(
        InlineKeyboardButton("PythonNotFound", url="https://t.me/pythonnotfound"),
        InlineKeyboardButton("Shaun", url="https://t.me/shaunc276"),
        InlineKeyboardButton("Submit Bugs", url="https://github.com/bharath1910/frankcrank/issues" )
        )

    return markup

def gen_markup():
    """
    Inline keyboard button layout, for /start
    """

    markup = InlineKeyboardMarkup()
    markup.row_width = 2

    markup.add(
        InlineKeyboardButton("Weather", callback_data="weather"),
        InlineKeyboardButton("Fun", callback_data="fun"),
        InlineKeyboardButton("Check out my source code", url="https://github.com/bharath1910/frankcrank" )
        )

    return markup

def fun_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3

    markup.add(
        InlineKeyboardButton("Memes", callback_data="memes"),
        InlineKeyboardButton("Aww", callback_data="aww"),
        InlineKeyboardButton("Joke", callback_data="joke"),
        InlineKeyboardButton("Shower Thoughts", callback_data="st")
    )

    return markup

def get_weather(WEATHER_API_KEY, latitude, longitude):
    """
    Function to get weather data.
    """

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
    city = result['name']
    final = {
        "main": main,
        "description": description,
        "temp": temp,
        "temp_min": temp_min,
        "temp_max": temp_max,
        "pressure": pressure,
        "humidity": humidity,
        "windspeed": windspeed,
        "wind_degree": wind_degree,
        "city": city
    }
    return final

def st_reddit():
    st = reddit.subreddit("Showerthoughts")
    top = st.top(limit = 50)

    submission = []

    for i in top:
        submission.append(i)
    
    return random.choice(submission)

def memes_reddit():
    memes = reddit.subreddit("memes")
    top = memes.top(limit=50)

    submission = []

    for i in top:
        submission.append(i)
    
    return random.choice(submission)

def aww_reddit():
    memes = reddit.subreddit("aww")
    top = memes.top("week",limit=50)

    submission = []

    for i in top:
        if "jpg" in i.url[len(i.url) - 3:] or "png" in i.url[len(i.url)-3]:
            submission.append(i)
    
        else:
            pass
    
    return random.choice(submission)
    
def jokes_reddit():
    jokes = reddit.subreddit("Jokes")
    top = jokes.top("week",limit=50)

    submission = [] 
    for i in top:
        if i.over_18:
            pass
        
        else:
            submission.append(i)

    return random.choice(submission)

# /start
@bot.message_handler(commands=['start'])
def message_handler(message):
    bot.send_message(message.chat.id, "👋 *Hi, I am Frank.* \n \n🌤 I can send the current weather in your locality. \n🐸 I can send memes ;) \n\n🎲 Maybe throw a dice? - /roll \n\n*Developers*\n@PythonNotFound\n@shaunc276", reply_markup=gen_markup())

# /help, sends help text
@bot.message_handler(commands=['help'])
def msg_handler(msg):
    bot.send_message(msg.chat.id,"👋 *Hi, I have 3 main functions.*\n\n *1. ⛅️ Get local weather*\n    - Send /start to me and click the weather button.\n    - Click the 📎 and send the location to get the weather data.\n    - *Note:* This will only works on Mobile.\n\n*2.🐸 Get desired memes!*\n    - This feature is not yet implemented\n\n*3.🎲 Roll em!*\n    - Send /roll to me and I will roll a dice for ya\n\nIf you happened to find any bugs, feel free to message *PythonNotFound* or *Shaun*, or open a new issue on the bot's GitHub Page.\n\n*Made with ❤️ using Python.*", reply_markup=help_markup())

# /help, sends help text
@bot.message_handler(commands=['help'])
def msg_handler(msg):
    bot.send_message(msg.chat.id,"👋 *Hi, I have 3 main functions.*\n\n *1. ⛅️ Get local weather*\n    - Send /start to me and click the weather button.\n    - Click the 📎 and send the location to get the weather data.\n    - *Note:* This will only works on Mobile.\n\n*2.🐸 Get desired memes!*\n    - This feature is not yet implemented\n\n*3.🎲 Roll em!*\n    - Send /roll to me and I will roll a dice for ya\n\nIf you happened to find any bugs, feel free to message *PythonNotFound* or *Shaun*, or open a new issue on the bot's GitHub Page.\n\n*Made with ❤️ using Python.*", reply_markup=help_markup())

# /roll, sends a dice
@bot.message_handler(commands=['roll'])
def send(msg):
    bot.send_dice(chat_id=msg.chat.id)

# /st, sends a shower thought
@bot.message_handler(commands=['st'])
def send(msg):
    bot.send_message(msg.chat.id,st_reddit().title)

@bot.message_handler(commands=['meme'])
def send(msg):
    memes = memes_reddit()
    bot.send_photo(msg.chat.id, memes.url, memes.title)

@bot.message_handler(commands=['aww'])
def send(msg):
    a = aww_reddit()
    bot.send_photo(msg.chat.id, a.url, a.title)

@bot.message_handler(commands=['joke'])
def send(msg):
    jokes = jokes_reddit()
    bot.send_message(msg.chat.id,f"*{jokes.title}*\n\n{jokes.selftext}")
    



def ms_km(num):
    """
    Function to convert m/s to km/h
    """

    return (math.floor(3.6 * num))

def degrees_to_direction(deg):
    """
    Function to convert degrees to direction.
    """
    
    if deg == 0:
        return ""

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

    result = dir_arr[int(((deg%360)//22.5))]
    return f"due *{result}*"


# Weather and memes query handler
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "weather":
        bot.send_message(call.message.chat.id, "Send the location.")

        @bot.message_handler(content_types=['location'])
        def handle_location(message):
            latitude = message.location.latitude
            longitude = message.location.longitude

            x = time.time()
            weather_result=get_weather(WEATHER_API_KEY, latitude, longitude)
            end = time.time()
            

            bot.send_message(message.chat.id,f"{weather_result['main']}, Expected {weather_result['description']} in {weather_result['city']}.\n\n*More Information:*\n    *-  Average Temperature* : {weather_result['temp']}C\n    *-  Minimum Temperature* : {weather_result['temp_min']}C\n    *-  Maximum Temperature* : {weather_result['temp_max']}C\n    *-  Atmospheric Pressure* : {weather_result['pressure']}hpa\n    *-  Humidity* : {weather_result['humidity']}%\n\nWind speed *{ms_km(weather_result['windspeed'])}km/h* {degrees_to_direction(weather_result['wind_degree'])}\nAPI Responce time : *{round(end-x,2)}s*")


    elif call.data == "fun":
        bot.send_message(call.message.chat.id, "Hey!, So you finally decided to have some fun.\n\n*- Memes:* Sends top memes of the day [/meme]!\n*- Aww:* Get a cute and cuddly picture! [/aww]\n*- Jokes:* Sends tops jokes [/jokes]\n*- Shower Thoughts:* Get a shower thought [/st]\n\nNew features coming soon, stay in touch :D", reply_markup=fun_markup())

    elif call.data == "st":
        bot.send_message(call.message.chat.id, st_reddit().title)
    
    elif call.data == "memes":
        meme = memes_reddit()
        bot.send_photo(call.message.chat.id,meme.url,meme.title)
    
    elif call.data == "aww":
        a = aww_reddit()
        bot.send_photo(call.message.chat.id, a.url,a.title)
    
    elif call.data == "joke":
        jokes = jokes_reddit()
        bot.send_message(call.message.chat.id,f"*{jokes.title}*\n\n{jokes.selftext}")
        


        

# polling section
bot.infinity_polling()