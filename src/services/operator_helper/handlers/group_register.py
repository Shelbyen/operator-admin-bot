from aiogram import Router, Bot
from aiogram.filters import ChatMemberUpdatedFilter, JOIN_TRANSITION
from aiogram.types import ChatMemberUpdated

from filters.chat_type import ChatTypeFilter
from schemas.chat_schema import ChatCreate
from services.admin_service import admin_service
from services.chat_service import chat_service

router = Router()
router.message.filter(ChatTypeFilter(is_group=True))


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION))
async def add_chat(event: ChatMemberUpdated, bot: Bot):
    if not await admin_service.exists(str(event.from_user.id)):
        await event.answer('Вы не админ!')
        await bot.leave_chat(event.chat.id)
        return
    await chat_service.create(ChatCreate(id=str(event.chat.id), name=event.chat.full_name))
    print(f'Новый чат!\nid: {event.chat.id}\nname: {event.chat.full_name}')
    await event.answer('Чат успешно добавлен!')
