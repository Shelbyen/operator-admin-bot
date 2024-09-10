from aiogram import Router
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message
from aiogram.utils.payload import decode_payload

from filters.chat_type import ChatTypeFilter
from schemas.chat_schema import ChatCreate
from services.admin_service import admin_service
from services.chat_service import chat_service

router = Router()
router.message.filter(ChatTypeFilter(is_group=True))


@router.message(CommandStart(deep_link=True))
async def add_chat(message: Message, command: CommandObject):
    args = command.args
    payload = decode_payload(args)
    if not await admin_service.check_invite(int(payload)):
        await message.answer('Истек срок действия ссылки!')
        return
    await chat_service.create(ChatCreate(id=message.chat.id, name=message.chat.full_name))
    print(f'Новый чат!\nid: {message.chat.id}\nname: {message.chat.full_name}')
    await message.answer('Чат успешно добавлен!')
