import re

from telebot import types
from telebot.callback_data import CallbackData, CallbackDataFilter
from datetime import date, datetime
import threading

class NotifyManager:
    def __init__(self, bot, file_manager):
        self.bot = bot
        self.file_manager = file_manager
        self.buttons = [
            {'id': 0, 'text': 'Поздравил.', 'value': 0},
            {'id': 1, 'text': 'Поздравлю позже.', 'value': 0}
        ]

    def notify_manager(self):
        bd_data = self.file_manager.get_all_data()
        today = date.today()
        for data in bd_data:
            for column in data:
                i = 0
                for row in range(len(data[column][0])):
                    try:
                        row_date = datetime.strptime(data[column][0][row]['date'], "%d.%m.%Y")
                    except ValueError:
                        row_date = datetime.strptime(data[column][0][row]['date'], "%d.%m")

                    if row_date.date().month == today.month and row_date.date().day == today.day:
                        if not data[column][0][row]['notify']:
                            self.buttons[0]['value'] = i
                            self.buttons[1]['value'] = i
                            keyboard_manager = KeyboardManager(self.bot, self.file_manager, self.buttons)
                            new_conn_thread = threading.Thread(target=keyboard_manager.show_keyboard(data[column][0][row]))
                            new_conn_thread.start()
                    i += 1


class KeyboardManager:
    def __init__(self, bot, file_manager, buttons):
        self.bot = bot
        self.file_manager = file_manager
        self.buttons = buttons
        self.buttons_factory = CallbackData('button_id', prefix='buttons')

        @bot.callback_query_handler(func=None, config=self.buttons_factory.filter())
        def products_callback(call: types.CallbackQuery):
            callback_data: dict = self.buttons_factory.parse(callback_data=call.data)
            button_data = callback_data['button_id'].strip('][').split(',')
            button_id, button_value = int(button_data[0]), int(button_data[1])
            button = self.buttons[button_id]
            if button_id == 0:
                print(button_value)
                self.file_manager.change_notify_status(call.from_user.id, button_value, True)
            elif button_id == 1:
                print(button_value)
                self.file_manager.change_notify_status(call.from_user.id, button_value, False)

            text = f"Отмечено как: {button['text']}"
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=text)

    def bd_keyboard(self):
        return types.InlineKeyboardMarkup(
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        text=button['text'],
                        callback_data=self.buttons_factory.new(button_id=[button["id"], button["value"]])
                    )
                ]
                for button in self.buttons
            ]
        )

    def show_keyboard(self, row):
        text = f'''Сегодня ДР у {row['name']}'''
        if row['nick']:
            text += f''', ник: {row['nick']}'''
        self.bot.send_message(row['id'], text, reply_markup=self.bd_keyboard())
