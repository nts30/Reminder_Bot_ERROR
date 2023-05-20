from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_kb = ReplyKeyboardMarkup(resize_keyboard=True).add('Добавить напоминание')

cancel_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(KeyboardButton('Отмена'))

choice_kb = ReplyKeyboardMarkup(resize_keyboard=True).row(KeyboardButton('Да'), KeyboardButton('Нет')).row(
    KeyboardButton('Отмена')
)
