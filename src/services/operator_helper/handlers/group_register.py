from aiogram import Router, Bot, F
from aiogram.filters import ChatMemberUpdatedFilter, JOIN_TRANSITION, LEAVE_TRANSITION
from aiogram.types import ChatMemberUpdated, Message

from ..filters.chat_type import ChatTypeFilter
from ..schemas.chat_schema import ChatCreate, ChatUpdate
from ..schemas.message_schema import MessageCreate
from ..services.admin_service import admin_service
from ..services.chat_service import chat_service
from ..services.message_service import message_service

router = Router()
router.my_chat_member.filter(ChatTypeFilter(is_group=True))
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


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=LEAVE_TRANSITION))
async def delete_chat(event: ChatMemberUpdated):
    await chat_service.delete(str(event.chat.id))
    print(f'Чат удален!\nid: {event.chat.id}\nname: {event.chat.full_name}')


@router.message(F.migrate_to_chat_id)
async def group_to_supegroup_migration(message: Message):
    chat_messages = await message_service.get_by_chat(chat_id=str(message.chat.id))
    await chat_service.delete(message.chat.id)
    await chat_service.create(ChatCreate(id=str(message.migrate_to_chat_id), name=message.chat.full_name))
    await message_service.create_many([MessageCreate(id=i.id,
                                                     chat_id=str(message.migrate_to_chat_id),
                                                     phone=i.phone,
                                                     message=i.message) for i in chat_messages])


@router.message(F.new_chat_title)
async def changing_chat_title(message: Message):
    await chat_service.update(pk=message.chat.id, model=ChatUpdate(name=message.chat.full_name))
