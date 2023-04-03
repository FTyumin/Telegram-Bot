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
    '/movie':'gives info about the movie',
    
    
}

BOT_TOKEN = os.environ.get('BOT_TOKEN')
API_TOKEN = os.environ.get('OMDB_API_KEY')

bot = telebot.TeleBot(BOT_TOKEN)



def get_movie(message):
    
   movie_title = message.text
   url = f"http://www.omdbapi.com/?apikey={API_TOKEN}&t={movie_title}"
   response = requests.get(url)
   if response.status_code == 200:
        movie_info = response.json()
        if movie_info["Response"] == "True":
            title = movie_info["Title"]
            year = movie_info["Year"]
            plot = movie_info["Plot"]
            rating = movie_info["imdbRating"]
            genre = movie_info["Genre"]
            director = movie_info["Director"]
            actors = movie_info["Actors"]
            poster = movie_info["Poster"]
            message_text = f"<b>Title:</b> {title}\n<b>Year:</b> {year}\n<b>Plot:</b> {plot}\n<b>IMDB Rating:</b> {rating}\n<b>Genre:</b> {genre}\n<b>Director:</b> {director}\n<b>Actors:</b> {actors}"
            bot.send_message(message.chat.id, message_text, parse_mode="HTML")
            if poster != "N/A":
                bot.send_photo(message.chat.id, poster)
            else:
                bot.send_message(message.chat.id, "Movie not found.")
        else:
            bot.send_message(message.chat.id, "Error getting movie information.")



@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,'Welcome to the movie bot! Please give a movie title')


@bot.message_handler(commands=['help'])
def send_welcome(message):
    response = "Here are the available commands:\n\n"
    for command, description in commands.items():
        response += f"{command} - {description}\n"
    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['movie'])
def movie_info(message):
    bot.send_message(message.chat.id, "Enter the title of the movie:")
    bot.register_next_step_handler(message, get_movie)



bot.infinity_polling()