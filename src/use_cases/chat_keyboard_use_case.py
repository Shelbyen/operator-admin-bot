from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.services.admin.schemas.chat_schema import ChatBase


def chunks(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]


def get_chat_keyboards(chats: List[ChatBase], command_num: str) -> List[InlineKeyboardMarkup]:
    kbs = []

    if chats is None:
        chats = []

    for chat_group in list(chunks(chats, 100)):
        kb = []
        for i in chat_group:
            kb.append(
                [InlineKeyboardButton(text=i.name,
                                      callback_data=f'{command_num}|{i.id}|0')])
        kbs.append(InlineKeyboardMarkup(inline_keyboard=kb))
    return kbs
