from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


def create_menu():
    kb = [[KeyboardButton(text='Отправить сообщение')]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите команду"
    )
    return keyboard


def back_to_choosing():
    kb = [[InlineKeyboardButton(text='Вернуться к выбору чата', callback_data=f'1|0|0')]]
    return InlineKeyboardMarkup(inline_keyboard=kb)
