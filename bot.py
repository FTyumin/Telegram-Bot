import os
import random
import requests

from dotenv import load_dotenv
import telebot
from telebot import types


load_dotenv()

commands = {
    '/start': 'Start the bot',
    '/help': 'View all available commands',
    '/button': 'Display a button',
    # Add more commands here
}

BOT_TOKEN = os.environ.get('BOT_TOKEN')
API_TOKEN = os.environ.get('OMDB_API_KEY')

bot = telebot.TeleBot(BOT_TOKEN)



def get_random_movie():
    
    url = f"https://www.omdbapi.com/?apikey={API_TOKEN}&t=Inception&plot=full"
    response = requests.get(url)
    
    data = response.json()
    title = data.get("Title")
    year = data.get("Year")
    imdb_id = data.get("imdbID")
    plot = data.get("Plot")
    return plot



@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,'Hello')
@bot.message_handler(commands=['button'])
def button_message(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Button")
    markup.add(item1)
    bot.send_message(message.chat.id,'Choose what do you need',reply_markup=markup)

@bot.message_handler(commands=['help'])
def send_welcome(message):
    response = "Here are the available commands:\n\n"
    for command, description in commands.items():
        response += f"{command} - {description}\n"
    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['recommend'])
def recommend(message):
    random_movie = get_random_movie()
    bot.send_message(message.chat.id, random_movie)



bot.infinity_polling()