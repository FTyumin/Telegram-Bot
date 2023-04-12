import os
import requests
from dotenv import load_dotenv
import telebot

# loads environment variables from a .env file located in the same directory as the script
load_dotenv()

commands = {
    "/start": "Start the bot",
    "/help": "View all available commands",
    "/movie": "Gives info about the movie",
    "/new":"Find out about new releases"
}

# retrieves the bot tokens from the environment variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_TOKEN = os.environ.get("OMDB_API_KEY")
API_TOKEN_TMDB = os.environ.get("TMDB_API_KEY")

# creates a new Telegram bot instance with the retrieved bot token
bot = telebot.TeleBot(BOT_TOKEN)

# function that retrieves information about a movie using the OMDB API and sends it to the user
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


# function that retrieves information about upcoming movies using the TMDB API and returns a list of up to three movies
def upcoming_movies():
    url = "https://api.themoviedb.org/3/movie/upcoming"
    params = {"api_key": API_TOKEN_TMDB, "language": "en-US", "page": 1}
    response = requests.get(url, params=params)
    movies = response.json()["results"]
    upcoming_movies = []
    counter = 0
    for movie in movies:
        if counter == 3:
            break
        upcoming_movies.append(movie)
        counter += 1
    return upcoming_movies

def trend():
    url = "https://api.themoviedb.org/3/trending/movie/week?"
    params = {"api_key": API_TOKEN_TMDB, "media_type": "movie", "page": 1}
    response = requests.get(url, params=params)
    movies = response.json()["results"]
    return movies



# decorator functions
@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(
        message.chat.id, "Welcome to the movie bot! Please give a movie title"
    )


@bot.message_handler(commands=["help"])
def send_welcome(message):
    response = "Here are the available commands:\n\n"
    for command, description in commands.items():
        response += f"{command} - {description}\n"
    bot.send_message(message.chat.id, response)


@bot.message_handler(commands=["movie"])
def movie_info(message):
    bot.send_message(message.chat.id, "Enter the title of the movie:")
    bot.register_next_step_handler(message, get_movie)


@bot.message_handler(commands=["new"])
def new_movies(message):
    upcoming = upcoming_movies()
    if not upcoming:
        bot.send_message(message.chat.id, "No upcoming movies.")
    else:
        for movie in upcoming:
            bot.send_message(
                message.chat.id,
                f"{movie['title']} ({movie['release_date']}) {movie['overview']}",
            )

@bot.message_handler(commands=["trend"])
def trend_movies(message):
    text = trend()
    bot.send_message(message.chat.id,text)


# starts the bot's polling loop, allowing it to receive and respond to user messages indefinitely
bot.infinity_polling()
