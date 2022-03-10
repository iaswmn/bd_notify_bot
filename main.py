import time
import threading
import re
from telebot import types, TeleBot
from telebot.custom_filters import AdvancedCustomFilter
from telebot.callback_data import CallbackData, CallbackDataFilter
from datetime import date, datetime
from config import BotSettings
from file_manager import FileManager
from notify import NotifyManager

bot = TeleBot(BotSettings.BOT_TOKEN.value)
file_manager = FileManager()
notify_manager = NotifyManager(bot, file_manager)

data_dict = {'id': '',
             'name': '',
             'date': '',
             'nick': None,
             'notify': False}

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
    bot.send_message(message.chat.id,
                     'Пример: Женя Программист, 01.01.1990, @test, 2 (это номер записи из запроса see)')
    bot.register_next_step_handler(message, check_message, 3)




def extract_arg(arg):
    return arg.split()[1:]


def check_message(message, type):
    global data_dict
    data_list = message.text.replace(" ", "").split(',')
    if len(data_list) >= 2:
        try:
            data_dict['id'] = message.from_user.id
            data_dict['name'] = data_list[0]
            data_dict['date'] = check_on_date(data_list[1])
            if len(data_list) == 3:
                data_dict['nick'] = check_on_nick(data_list[2])
            prepare_data_to_save(data_dict, type)
        except Exception as e:
            bot.send_message(message.chat.id, str(e))
            bot.register_next_step_handler(message, check_message, type)
    else:
        bot.send_message(message.chat.id, 'bad request, try agin...')
        bot.register_next_step_handler(message, check_message, type)


def check_on_date(date_from_msg):
    try:
        date_from_msg1 = re.sub("[-|/.]", ".", date_from_msg)
        datetime.strptime(date_from_msg1, "%d.%m.%Y")
        return date_from_msg1
    except ValueError:
        raise Exception('Bad date format.')


def check_on_nick(nick_from_msg):
    if nick_from_msg[0] != '@':
        raise Exception('Nick must start from @.')
    return nick_from_msg


def prepare_data_to_save(bd_dict, save_type):
    if save_type == 2:
        file_manager.save_data_to_file(bd_dict)
        bot.send_message(bd_dict['id'], "Запись добалена!")
    elif save_type == 3:
        update_row(bd_dict['id'], bd_dict, data[3])


def show_all_bd_data_for_id(from_id):
    data = file_manager.get_data_by_id(from_id)
    if len(data) != 0:
        i = 0
        for row in data:
            message_to_send = f'''№{i} - {row['name']}, {row['date']}, {row['nick']}'''
            bot.send_message(from_id, message_to_send)
            i += 1
    else:
        bot.send_message(from_id, 'Нет сохраненных записей!')


def update_row(from_id, data, row_number):
    file_manager.update_data_by_id_and_i(from_id, int(row_number), data)
    bot.send_message(from_id, "Updated!")


def delete_row(from_id, message):
    args_dict = extract_arg(message.text)
    file_manager.delete_data_by_id_and_i(from_id, int(args_dict[0]))
    bot.send_message(from_id, "Запись удалена!")


def notify_worker():
    notify_manager.notify_manager()
    threading.Timer(100.0, notify_worker).start()


class ProductsCallbackFilter(AdvancedCustomFilter):
    key = 'config'

    def check(self, call: types.CallbackQuery, config: CallbackDataFilter):
        return config.check(query=call)


bot.add_custom_filter(ProductsCallbackFilter())
notify_worker()
bot.polling(none_stop=True, interval=0)
