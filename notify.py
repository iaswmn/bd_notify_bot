from telebot import types
from telebot.callback_data import CallbackData, CallbackDataFilter
from datetime import date, datetime


class NotifyManager:
    def __init__(self, bot, file_manager):
        self.bot = bot
        self.file_manager = file_manager
        self.buttons = [
            {'id': 0, 'text': 'Поздравил!', 'value': 0},
            {'id': 1, 'text': 'Поздравлю позже!', 'value': 0}
        ]
        self.buttons_factory = CallbackData('button_id', prefix='buttons')

        @bot.callback_query_handler(func=None, config=self.buttons_factory.filter())
        def products_callback(call: types.CallbackQuery):
            callback_data: dict = self.buttons_factory.parse(callback_data=call.data)
            button_id = int(callback_data['button_id'])
            button = self.buttons[button_id]

            if button_id == 0:
                self.file_manager.change_notify_status(call.from_user.id, button['value'], False)
            elif button_id == 1:
                self.file_manager.change_notify_status(call.from_user.id, button['value'], True)

            text = f"Отмечено как: {button['text']}"
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=text)

    def notify_manager(self):
        bd_data = self.file_manager.get_all_data()
        for row in bd_data:
            row_date = datetime.strptime(row['date'], "%d.%m.%Y")
            today = date.today()
            if row_date.date().month == today.month and row_date.date().day == today.day:
                print(13)
                self.show_keyboard(row)

    def bd_keyboard(self):
        return types.InlineKeyboardMarkup(
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        text=button['text'],
                        callback_data=self.buttons_factory.new(button_id=button["id"])
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

