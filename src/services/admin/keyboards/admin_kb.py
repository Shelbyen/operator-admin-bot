from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

from ..schemas.message_schema import MessageBase
from ..services.operator_service import operator_service


async def create_admin_choosing():
    all_admins = await operator_service.filter()
    if all_admins is None:
        all_admins = []
    a = sorted(all_admins, key=lambda x: x.name.lower())
    kb = []
    for i in a:
        kb.append(
            [InlineKeyboardButton(text=i.name,
                                  callback_data=f'1|{i.id}|0')])
    return InlineKeyboardMarkup(inline_keyboard=kb)


def create_menu(is_super_admin: bool = False):
    kb = [
        [
            KeyboardButton(text="Добавить чаты"),
            KeyboardButton(text="Удалить чаты")
        ],
        [
            KeyboardButton(text="Добавить операторов"),
            KeyboardButton(text="Удалить операторов")
        ],
        [KeyboardButton(text='Удалить сообщение')]
    ]

    if is_super_admin:
        kb.append([KeyboardButton(text="Отправить во все чаты")])

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите команду"
    )
    return keyboard


def deleting_messages_kb(messages: List[MessageBase]):
    kb = []
    for message in messages:
        kb.append([InlineKeyboardButton(text=f'8{message.phone}', callback_data=f'4|{message.id}|0')])
    kb.append([InlineKeyboardButton(text='Вернуться к выбору чата', callback_data='5')])
    return InlineKeyboardMarkup(inline_keyboard=kb)


def back_button():
    kb = [[InlineKeyboardButton(text='Назад', callback_data='back')]]
    return InlineKeyboardMarkup(inline_keyboard=kb)
