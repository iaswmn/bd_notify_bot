import telebot
from config import BotSettings

bot = telebot.TeleBot(BotSettings.BOT_TOKEN.value)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'hi')


@bot.message_handler(commands=['add'])
def add(message):
    bot.send_message(message.chat.id, 'Example...')
    bot.register_next_step_handler(message, check_message)

def check_message(message):
    if len(message.text.replace(" ", "").split(',')) != 3:
        try:
            valid_date = time.strptime(date, '%m/%d/%Y')
        except ValueError:
            print('Invalid date!')
        bot.send_message(message.chat.id, 'bad request, try agin...')
        bot.register_next_step_handler(message, check_message)
    else:
        bot.send_message(message.chat.id, 'okiokioki')


bot.polling(none_stop=True, interval=0)