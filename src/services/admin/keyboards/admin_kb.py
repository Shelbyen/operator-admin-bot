from math import ceil

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

from services.chat_service import chat_service
from services.operator_service import operator_service


async def create_chat_choosing(page):
    all_chats = await chat_service.filter()
    if all_chats is None:
        all_chats = []

    a = all_chats[page * 5: page * 5 + 5]
    is_last_page = page == ceil(len(all_chats) / 5) - 1
    kb = []
    for i in a:
        kb.append(
            [InlineKeyboardButton(text=i.name,
                                  callback_data=f'4|{i.id}|{page}')])
    kb.append(
        [InlineKeyboardButton(text=('<-' if page > 0 else 'X'),
                              callback_data=f"3|0|{page - 1 if page > 0 else '-1'}"),
         InlineKeyboardButton(text="Закончить", callback_data="cancel"),
         InlineKeyboardButton(text=("->" if not is_last_page else "X"),
                              callback_data=f"3|0|{page + 1 if not is_last_page else '-1'}", ),
         ]
    )
    return InlineKeyboardMarkup(inline_keyboard=kb)


async def create_admin_choosing(page):
    all_admins = await operator_service.filter()
    if all_admins is None:
        all_admins = []
    a = all_admins[page * 5: page * 5 + 5]
    is_last_page = page == ceil(len(all_admins) / 5) - 1
    kb = []
    for i in a:
        kb.append(
            [InlineKeyboardButton(text=i.name,
                                  callback_data=f'6|{i.id}|{page}')])
    kb.append(
        [InlineKeyboardButton(text=('<-' if page > 0 else 'X'),
                              callback_data=f"5|0|{page - 1 if page > 0 else '-1'}"),
         InlineKeyboardButton(text="Закончить", callback_data="cancel"),
         InlineKeyboardButton(text=("->" if not is_last_page else "X"),
                              callback_data=f"5|0|{page + 1 if not is_last_page else '-1'}", ),
         ]
    )
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
