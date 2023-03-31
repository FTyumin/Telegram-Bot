import os
import telebot
from telebot import types
from dotenv import load_dotenv


load_dotenv()

commands = {
    '/start': 'Start the bot',
    '/help': 'View all available commands',
    '/button': 'Display a button',
    # Add more commands here
}

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)



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



bot.infinity_polling()