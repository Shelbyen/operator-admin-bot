from aiogram import Router
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message
from aiogram.utils.payload import decode_payload

from .operator import menu
from filters.chat_type import ChatTypeFilter
from services.admin_service import admin_service
from schemas.operator_schema import OperatorCreate
from services.operator_service import operator_service

router = Router()
router.message.filter(ChatTypeFilter())


@router.message(CommandStart(deep_link=True))
async def add_operator(message: Message, command: CommandObject):
    args = command.args
    payload = decode_payload(args)
    if not await admin_service.check_invite(int(payload)):
        await message.answer('Пригласивший - не админ или истек срок действия!')
        return
    name = message.from_user.full_name if message.from_user.username is None else message.from_user.username
    await operator_service.create(OperatorCreate(id=message.from_user.id, name=name))
    print(f'Новый оператор!\nid: {message.from_user.id}\nusername: {message.from_user.username}')
    await message.answer('Вы теперь оператор!')
    await menu(message)
