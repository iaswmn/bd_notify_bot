import time

import telebot
from config import BotSettings
from file_manager import FileManager

bot = telebot.TeleBot(BotSettings.BOT_TOKEN.value)
file_manager = FileManager()


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'hi')


@bot.message_handler(commands=['add'])
def add(message):
    bot.send_message(message.chat.id, 'Example: Женя Программист, 01.01.1990, @test')
    bot.register_next_step_handler(message, check_message, 2)


@bot.message_handler(commands=['see'])
def see(message):
    show_all_bd_data_for_id(message.from_user.id)

@bot.message_handler(commands=['cut'])
def cut(message):
    delete_row(message.from_user.id, message)

@bot.message_handler(commands=['change'])
def change(message):
    bot.send_message(message.chat.id, 'Example: Женя Программист, 01.01.1990, @test, 2 (это номер записи из запроса see)')
    bot.register_next_step_handler(message, check_message, 3)


def extract_arg(arg):
    return arg.split()[1:]


def check_message(message, type):
    data_list = message.text.replace(" ", "").split(',')
    if len(data_list) >= 3:
        try:
            check_on_date(data_list[1])
            check_on_nick(data_list[2])
            prepare_data_to_save(message.from_user.id, data_list, type)
        except Exception as e:
            bot.send_message(message.chat.id, str(e))
            bot.register_next_step_handler(message, check_message, type)
    else:
        bot.send_message(message.chat.id, 'bad request, try agin...')
        bot.register_next_step_handler(message, check_message, type)


def check_on_date(date_from_msg):
    try:
        time.strptime(date_from_msg, '%d.%m.%Y')
    except ValueError:
        raise Exception('Bad date format.')


def check_on_nick(nick_from_msg):
    if nick_from_msg[0] != '@':
        raise Exception('Nick must start from @.')


def prepare_data_to_save(from_id, data, save_type):
    bd_dict = {'id': from_id,
               'name': data[0],
               'date': data[1],
               'nick': data[2]}
    if save_type == 2:
        file_manager.save_data_to_file(bd_dict)
        bot.send_message(from_id, "Added!")
    elif save_type == 3:
        update_row(from_id, bd_dict, data[3])


def show_all_bd_data_for_id(from_id):
    data = file_manager.get_data_by_id(from_id)
    i = 0
    for row in data:
        message_to_send = f'''№{i} - {row['name']}, {row['date']}, {row['nick']}'''
        bot.send_message(from_id, message_to_send)
        i += 1


def update_row(from_id, data, row_number):
    file_manager.update_data_by_id_and_i(from_id, int(row_number), data)
    bot.send_message(from_id, "Updated!")


def delete_row(from_id, message):
    args_dict = extract_arg(message.text)
    file_manager.delete_data_by_id_and_i(from_id, int(args_dict[0]))
    bot.send_message(from_id, "Deleted!")


bot.polling(none_stop=True, interval=0)
