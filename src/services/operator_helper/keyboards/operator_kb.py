from math import ceil

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

from services.chat_service import chat_service


async def create_chat_choosing():
    all_chats = await chat_service.filter()
    if all_chats is None:
        all_chats = []

    a = sorted(all_chats, key=lambda x: x.name.lower())
    kb = []
    for i in a:
        kb.append(
            [InlineKeyboardButton(text=i.name,
                                  callback_data=f'0|{i.id}|0')])
    return InlineKeyboardMarkup(inline_keyboard=kb)


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
