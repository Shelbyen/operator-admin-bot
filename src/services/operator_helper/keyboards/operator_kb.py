from datetime import datetime, timedelta
from math import ceil

from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton




async def create_chat_choosing(all_chats):
    if all_chats is None:
        all_chats = []

    a = sorted(all_chats, key=lambda x: x.name.lower())
    kb = []
    for i in a:
        if datetime.now() - i.updated_at > timedelta(minutes=15):
            chat_info = await bot.get_chat(i.id)
            if chat_info.full_name != i.name:
                chat_service.update(pk=i.id, model=ChatUpdate(name=chat_info.full_name))
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
