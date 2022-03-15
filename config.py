from enum import Enum


class BotSettings(Enum):
    BOT_TOKEN = '5137855939:AAFSKgAGgBrTPdLu7qX_86yEXRkwGiDe0do'


class BotText(Enum):
    START_COMMAND = '''Доступные команды:
/add - добавить напоминание о поздравлении
/see - посмотреть список добавленных напоминаний
/change - изменить данные
/cut - удалить
'''
    EXAMPLE_TEXT = '''Пример: Женя Программист, 01.01.1990, @test'''
    CUT_COMMAND ='''Введите номер записи для удаления или номера записей через ",".'''
    CHANGE_COMMAND = '''Введите номер записи для изменения.'''
    NOT_VALID_DATA = '''Hе удалось добавить, проверьте правильность ввода по примеру: Имя, 01.01.1990, @nick. Обратите внимание, что значения должны отделяться символом запятой ", ".'''
    DATE_ERROR = '''Неверный формат даты.'''
    NICK_ERROR = '''Nick must start from @.'''
    SUCCESS_ADDED = '''Запись успешно добалена!'''
    SUCCESS_EDITED = '''Запись успешно изменена!'''
    SUCCESS_DELETED = '''Запись успешно удалена!'''
    NO_SAVED_DATA = '''Нет сохраненных записей.'''
    BAD_ROW_NUMBER = ''''Неверно введен номер записи.'''