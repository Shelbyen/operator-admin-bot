from datetime import datetime, timedelta, timezone

from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

from ..services.chat_service import chat_service
from ..schemas.chat_schema import ChatUpdate

async def create_chat_choosing(all_chats, bot: Bot):
    if all_chats is None:
        all_chats = []

    kb = []
    for i in all_chats:
        if datetime.now(timezone.utc) - i.updated_at > timedelta(hours=1):
            chat_info = await bot.get_chat(i.id)
            if chat_info.full_name != i.name:
                i.name = chat_info.full_name
                print(f'Change chat name from {i.name} to {chat_info.full_name}')
            await chat_service.update(pk=i.id, model=ChatUpdate(name=i.name, updated_at=datetime.now()))
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
