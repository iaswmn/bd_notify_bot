import telebot
from config import BotSettings

bot = telebot.TeleBot(BotSettings.BOT_TOKEN.value)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'hi')


@bot.message_handler(commands=['add'])
def add(message):
    bot.send_message(message.chat.id, 'Example...')


bot.polling(none_stop=True, interval=0)