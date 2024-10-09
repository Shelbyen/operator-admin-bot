from math import ceil

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

from services.chat_service import chat_service
from services.operator_service import operator_service


async def create_chat_choosing():
    all_chats = await chat_service.filter()
    if all_chats is None:
        all_chats = []

    a = sorted(all_chats, key=lambda x: x.name.lower())
    kb = []
    for i in a:
        kb.append(
            [InlineKeyboardButton(text=i.name, callback_data=f'4|{i.id}|0')])
    return InlineKeyboardMarkup(inline_keyboard=kb)


async def create_admin_choosing():
    all_admins = await operator_service.filter()
    if all_admins is None:
        all_admins = []
    a = sorted(all_admins, key=lambda x: x.name.lower())
    kb = []
    for i in a:
        kb.append(
            [InlineKeyboardButton(text=i.name,
                                  callback_data=f'6|{i.id}|0')])
    return InlineKeyboardMarkup(inline_keyboard=kb)


def create_menu():
    kb = [
        [
            KeyboardButton(text="Добавить чаты"),
            KeyboardButton(text="Удалить чаты")
        ],
        [
            KeyboardButton(text="Добавить операторов"),
            KeyboardButton(text="Удалить операторов")
        ]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите команду"
    )
    return keyboard
