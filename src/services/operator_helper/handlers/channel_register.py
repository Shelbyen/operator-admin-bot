from aiogram import Router, Bot, F
from aiogram.filters import ChatMemberUpdatedFilter, JOIN_TRANSITION, LEAVE_TRANSITION
from aiogram.types import ChatMemberUpdated, Message

from src.services.operator_helper.filters.chat_type import ChatTypeFilter
from src.services.operator_helper.schemas.chat_schema import ChatCreate, ChatUpdate
from src.services.operator_helper.services.admin_service import admin_service
from src.services.operator_helper.services.chat_service import chat_service

router = Router()
router.my_chat_member.filter(ChatTypeFilter(is_channel=True))
router.message.filter(ChatTypeFilter(is_channel=True))


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION))
async def add_channel(event: ChatMemberUpdated, bot: Bot):
    if not await admin_service.exists(str(event.from_user.id)):
        await bot.leave_chat(event.chat.id)
        return
    await chat_service.create(ChatCreate(id=str(event.chat.id), name=event.chat.full_name))
    print(f'Новый канал!\nid: {event.chat.id}\nname: {event.chat.full_name}')


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=LEAVE_TRANSITION))
async def add_chat(event: ChatMemberUpdated):
    await chat_service.delete(str(event.chat.id))
    print(f'Канал удален!\nid: {event.chat.id}\nname: {event.chat.full_name}')


@router.message(F.migrate_to_chat_id)
async def group_to_supegroup_migration(message: Message):
    await chat_service.delete(message.chat.id)
    await chat_service.create(ChatCreate(id=str(message.migrate_to_chat_id), name=message.chat.full_name))


@router.message(F.new_chat_title)
async def changing_chat_title(message: Message):
    await chat_service.update(pk=message.chat.id, model=ChatUpdate(name=message.chat.full_name))
