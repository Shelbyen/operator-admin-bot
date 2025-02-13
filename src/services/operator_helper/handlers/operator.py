from typing import Optional, List

from aiogram import Router, F
from aiogram.filters import Command, StateFilter, or_f, and_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, InputMediaPhoto, InputMediaDocument, InputMediaVideo, InputMediaAudio, \
    InputMediaAnimation
from phonenumbers import PhoneNumberMatcher

from ..filters.chat_type import ChatTypeFilter
from ..keyboards.operator_kb import *
from ..schemas.message_schema import MessageCreate
from ..services.chat_service import chat_service
from ..services.message_service import message_service

router = Router()
router.message.filter(ChatTypeFilter())


def chunks(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]


start_message = "Отправить сообщение - выпадает список подключенных чатов, после нажатия данный чат будет выбран. Далее потребует сообщение. После успешной отправки бот выдаст соответсвующее сообщение."


class OrderSend(StatesGroup):
    write_text = State()
    choosing_chats = State()


@router.callback_query(F.data == 'cancel')
async def cancel(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.clear()


@router.message(Command('start'))
async def menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(start_message, reply_markup=create_menu())
    await activate_sender(message, state)


@router.message(or_f(StateFilter(None), and_f(F.text.contains('Отправить сообщение'), OrderSend.write_text)))
async def activate_sender(message: Message, state: FSMContext):
    all_chats = sorted(await chat_service.filter(limit=300), key=lambda x: x.name.lower())
    messages = []
    for chat_group in list(chunks(all_chats, 100)):
        m = await message.answer("Выберите подключенный чат:",
                                 reply_markup=await create_chat_choosing(chat_group, message.bot))
        messages.append(m.message_id)
    await state.update_data({'messages': messages})
    await state.set_state(OrderSend.choosing_chats)


@router.callback_query(F.data[0] == '1')
async def choosing_chats(call: CallbackQuery, state: FSMContext):
    await state.set_data({})
    all_chats = sorted(await chat_service.filter(limit=300), key=lambda x: x.name.lower())
    messages = []
    for i, chat_group in enumerate(list(chunks(all_chats, 100))):
        if i == 0:
            m = await call.message.edit_text("Выберите подключенный чат:",
                                             reply_markup=await create_chat_choosing(chat_group, call.bot))
        else:
            m = await call.message.answer("Выберите подключенный чат:",
                                          reply_markup=await create_chat_choosing(chat_group, call.bot))
        messages.append(m.message_id)
    await state.update_data({'messages': messages})
    await state.set_state(OrderSend.choosing_chats)


@router.callback_query(OrderSend.choosing_chats, F.data[0] == '0')
async def active_mail_message(call: CallbackQuery, state: FSMContext):
    chat = await chat_service.get(call.data.split('|')[1])
    state_data = await state.get_data()
    messages = state_data['messages']
    await state.update_data({'chat_id': int(call.data.split('|')[1])})
    for i in messages:
        await call.bot.delete_message(call.from_user.id, i)
    await call.message.answer(f"Выбранный чат: {chat.name}\nТеперь отправьте ваше сообщение",
                              reply_markup=back_to_choosing())
    await state.set_state(OrderSend.write_text)


@router.message(OrderSend.write_text)
async def choosing_chats(message: Message, state: FSMContext, album: Optional[List[Message]] = None):
    # await state.set_state(OrderSend.choosing_chats)
    chat_id = (await state.get_data())["chat_id"]
    if album:
        media_group = []
        for msg in album:
            if msg.photo:
                file_id = msg.photo[-1].file_id
                media_group.append(InputMediaPhoto(media=file_id, caption=msg.caption))
            else:
                obj_dict = msg.model_dump()
                file_id = obj_dict[msg.content_type]['file_id']
                if msg.document:
                    media_group.append(InputMediaDocument(media=file_id, caption=msg.caption))
                elif msg.video:
                    media_group.append(InputMediaVideo(media=file_id, caption=msg.caption))
                elif msg.audio:
                    media_group.append(InputMediaAudio(media=file_id, caption=msg.caption))
                elif msg.animation:
                    media_group.append(InputMediaAnimation(media=file_id, caption=msg.caption))
        # await state.set_data({'message': media_group, 'sent': []})
        send_message = (await message.bot.send_media_group(chat_id, media_group))[0]
    else:
        send_message = await message.copy_to(chat_id)
    numbers = [match.number.national_number for match in PhoneNumberMatcher(message.text, 'GB')]
    print(numbers)
    await message_service.create_many(
        [MessageCreate(id=str(send_message.message_id), chat_id=str(chat_id), phone=str(number), message=message.text) for
         number in numbers])

    await message.answer('Сообщение успешно отправлено!')
    await state.clear()
    await activate_sender(message, state)
