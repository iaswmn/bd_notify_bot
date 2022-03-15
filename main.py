import time
import threading
import re
from telebot import types, TeleBot
from telebot.custom_filters import AdvancedCustomFilter
from telebot.callback_data import CallbackData, CallbackDataFilter
from datetime import date, datetime
from config import BotSettings, BotText
from file_manager import FileManager
from notify import NotifyManager

bot = TeleBot(BotSettings.BOT_TOKEN.value)
file_manager = FileManager()
notify_manager = NotifyManager(bot, file_manager)

edit_row_i = 0
data_dict = {'id': '',
             'name': '',
             'date': '',
             'nick': None,
             'notify': False}


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, BotText.START_COMMAND.value)


@bot.message_handler(commands=['add'])
def add(message):
    bot.send_message(message.chat.id, BotText.EXAMPLE_TEXT.value)
    bot.register_next_step_handler(message, check_message, 2)


@bot.message_handler(commands=['see'])
def see(message):
    show_all_bd_data_for_id(message.from_user.id)


@bot.message_handler(commands=['cut'])
def cut(message):
    try:
        bot.send_message(message.chat.id, BotText.CUT_COMMAND.value)
        show_all_bd_data_for_id(message.from_user.id)
        bot.register_next_step_handler(message, validate_row_number, 'cut')
    except Exception as e:
        bot.send_message(message.chat.id, str(e))


@bot.message_handler(commands=['change'])
def change(message):
    try:
        bot.send_message(message.chat.id, BotText.CHANGE_COMMAND.value)
        bot.register_next_step_handler(message, validate_row_number, 'change')
    except Exception as e:
        bot.send_message(message.chat.id, str(e))


# def extract_arg(arg):
#     args_list = arg.split()[1:]
#     if len(args_list) == 0:
#         raise Exception('Неверно введеная команда.')
#     return arg.split()[1:]


def check_message(message, type):
    if not message_is_command(message):
        global data_dict
        data_list = message.text.replace(" ", "").split(',')
        if len(data_list) >= 2:
            try:
                data_dict['id'] = message.from_user.id
                data_dict['name'] = data_list[0]
                data_dict['date'] = check_on_date(data_list[1])
                if len(data_list) >= 3:
                    data_dict['nick'] = check_on_nick(data_list[2])
                prepare_data_to_save(data_dict, type)
            except Exception as e:
                bot.send_message(message.chat.id, str(e))
                bot.register_next_step_handler(message, check_message, type)
        else:
            bot.send_message(message.chat.id, BotText.NOT_VALID_DATA.value)
            bot.register_next_step_handler(message, check_message, type)


def check_on_date(date_from_msg):
    try:
        re_date_list = re.sub("[-|/.]", ".", date_from_msg).split('.')
        re_date = '.'.join([str(elem) for elem in re_date_list])
        if len(re_date_list) == 2:
            datetime.strptime(re_date, "%d.%m")
        elif len(re_date_list) == 3:
            if len(re_date_list[2]) == 2:
                re_date_list[2] = '19' + re_date_list[2]
                re_date = '.'.join([str(elem) for elem in re_date_list])
            datetime.strptime(re_date, "%d.%m.%Y")
        return re_date
    except ValueError:
        raise Exception(BotText.DATE_ERROR.value)


def check_on_nick(nick_from_msg):
    if nick_from_msg[0] != '@':
        raise Exception(BotText.NICK_ERROR.value)
    return nick_from_msg


def prepare_data_to_save(bd_dict, save_type):
    if save_type == 2:
        file_manager.save_data_to_file(bd_dict)
        bot.send_message(bd_dict['id'], BotText.SUCCESS_ADDED.value)
    elif save_type == 3:
        update_row(bd_dict['id'], bd_dict, edit_row_i)


def show_all_bd_data_for_id(from_id):
    data = file_manager.get_data_by_id(from_id)
    if len(data) != 0:
        i = 0
        for row in data:
            message_to_send = f'''№{i} - {row['name']}, {row['date']}, {row['nick']}'''
            bot.send_message(from_id, message_to_send)
            i += 1
    else:
        bot.send_message(from_id, BotText.NO_SAVED_DATA.value)


def validate_row_number(message, command_type):
    if not message_is_command(message):
        global edit_row_i
        data = message.text
        if data.isdigit():
            if command_type == 'change':
                edit_row_i = int(data)
                bot.send_message(message.chat.id, BotText.EXAMPLE_TEXT.value)
                bot.register_next_step_handler(message, check_message, 3)
            elif command_type == 'cut':
                delete_row(message.from_user.id, int(data))
        elif ',' in data:
            numbers_list = message.text.replace(" ", "").split(',')
            for num in numbers_list:
                if not num.isdigit():
                    raise Exception(BotText.BAD_ROW_NUMBER.value)

            numbers_list = list(map(int, numbers_list))
            numbers_list.sort(reverse=True)
            for i in numbers_list:
                delete_row(message.from_user.id, i)
        else:
            raise Exception(BotText.BAD_ROW_NUMBER.value)


def update_row(from_id, data, row_number):
    result = file_manager.update_data_by_id_and_i(from_id, int(row_number), data)
    if result:
        bot.send_message(from_id, BotText.SUCCESS_EDITED.value)
    else:
        bot.send_message(from_id, BotText.NO_SAVED_DATA.value)


def delete_row(from_id, row_number):
    try:
        result = file_manager.delete_data_by_id_and_i(from_id, row_number)
        if result:
            bot.send_message(from_id, BotText.SUCCESS_DELETED.value)
        else:
            bot.send_message(from_id, BotText.NO_SAVED_DATA.value)
    except Exception as e:
        bot.send_message(from_id, str(e))


def notify_worker():
    notify_manager.notify_manager()
    threading.Timer(100.0, notify_worker).start()


class ProductsCallbackFilter(AdvancedCustomFilter):
    key = 'config'

    def check(self, call: types.CallbackQuery, config: CallbackDataFilter):
        return config.check(query=call)


def message_is_command(message):
    if message.text == '/start':
        start(message)
        return True
    elif message.text == '/add':
        add(message)
        return True
    elif message.text == '/cut':
        cut(message)
        return True
    elif message.text == '/change':
        change(message)
        return True
    elif message.text == '/see':
        see(message)
        return True
    else:
        return False


bot.add_custom_filter(ProductsCallbackFilter())
notify_worker()
bot.polling(none_stop=True, interval=0)
