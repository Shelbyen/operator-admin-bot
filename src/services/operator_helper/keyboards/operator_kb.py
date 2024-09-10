from math import ceil

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

from services.chat_service import chat_service


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
                                  callback_data=f'0|{i.id}|{page}')])
    kb.append(
        [InlineKeyboardButton(text=('<-' if page > 0 else 'X'),
                              callback_data=f"1|0|{page - 1 if page > 0 else '-1'}"),
         InlineKeyboardButton(text="Закончить", callback_data="cancel"),
         InlineKeyboardButton(text=("->" if not is_last_page else "X"),
                              callback_data=f"1|0|{page + 1 if not is_last_page else '-1'}", ),
         ]
    )
    return InlineKeyboardMarkup(inline_keyboard=kb)


def create_menu():
    kb = [[KeyboardButton(text='Отправить сообщение')]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите команду"
    )
    return keyboard


def back_to_choosing(page):
    kb = [[InlineKeyboardButton(text='Вернуться к выбору чата', callback_data=f'1|0|{page}')]]
    return InlineKeyboardMarkup(inline_keyboard=kb)
