from typing import Optional, List

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, InputMediaDocument, InputMediaVideo, InputMediaAudio, \
    InputMediaAnimation
from aiogram.utils.deep_linking import create_deep_link

from filters.chat_type import ChatTypeFilter
from keyboards.admin_kb import create_chat_choosing, create_admin_choosing, create_menu, back_button
from services.admin_service import admin_service
from services.chat_service import chat_service
from services.operator_service import operator_service

router = Router()
router.message.filter(ChatTypeFilter())


class SendMessageToAll(StatesGroup):
    write_text = State()

def chunks(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]


start_message = "**Добавить чаты** - по нажатию на кнопку бот дает ссылку на добавления чатов, при нажатии на нее автоматически откроется меню TG с выбором чатов. После выбора чата необходимо просто нажат на кнопку 'Добавить бота' не добавляю ему каких либо привилегий. После добавления бот должен написать в чат 'Чат успешно добавлен'.\n\n**Удалить чаты** - по нажатию на кнопку выпадет меню со всеми подключенными чатами. При нажатии на чат он автоматически удалится.\n\n**Добавить операторов** - по нажатию выдаст ссылку-приглашение. Срок действия ссылки - 15 минут, после этого необходимо снова создать ссылку.\n\n**Удалить операторов** - по нажатию выпадает меню со всеми операторами. При нажатии удаляет оператора.\n"


@router.callback_query(F.data == 'cancel')
async def cancel(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Ок")
    await state.clear()


@router.message(Command('start'))
async def start_bot(message: Message | CallbackQuery):
    await message.bot.send_message(message.from_user.id, start_message, reply_markup=create_menu(), parse_mode="Markdown")


@router.message(F.text.lower() == 'добавить чаты')
async def add_chat(message: Message):
    link = 'https://t.me/helper_operator_bot?startgroup='
    await message.answer(f'Используйте ссылку ниже чтобы добавить бота в группу: {link}')


@router.message(F.text.lower() == "добавить операторов")
async def get_ref(message: Message):
    admin = await admin_service.get_with_update(str(message.from_user.id))
    link = create_deep_link('helper_operator_bot', 'start', str(admin.invite_hash), encode=True)
    await message.answer(f"Ссылка для приглашения оператора: {link}")


@router.message(F.text.lower() == "удалить чаты")
async def choosing_delete_chat_start(message: Message):
    for chat_group in list(chunks(sorted(await chat_service.filter(limit=500), key=lambda x: x.name.lower()), 100)):
        await message.answer("Выберите чаты которые хотите удалить:",
                             reply_markup=await create_chat_choosing(chat_group))


@router.callback_query(F.data[0] == '4')
async def delete_chat(call: CallbackQuery):
    chat_id = int(call.data.split('|')[1])

    await chat_service.delete(str(chat_id))
    await choosing_delete_chat_start(call.message)


@router.message(F.text.lower() == "удалить операторов")
async def choosing_delete_admin_start(message: Message):
    await message.answer("Выберите операторов которых хотите удалить:",
                         reply_markup=await create_admin_choosing())


@router.callback_query(F.data[0] == '6')
async def delete_admin(call: CallbackQuery):
    operator_id = call.data.split('|')[1]

    await operator_service.delete(operator_id)
    await choosing_delete_admin_start(call.message)


@router.message(F.text.lower() == "отправить во все чаты")
async def send_all_command(message: Message, state: FSMContext):
    await state.set_state(SendMessageToAll.write_text)
    message = await message.answer(f"Отправьте ваше сообщение", reply_markup=back_button())
    await state.update_data({'message_id': message.message_id})


@router.message(SendMessageToAll.write_text)
async def choosing_chats(message: Message, state: FSMContext, album: Optional[List[Message]] = None):
    message_id = (await state.get_data())['message_id']
    chats = await chat_service.filter(limit=500)
    if album:
        media_group = []
        for msg in album:
            if msg.photo:
                file_id = msg.photo[-1].file_id
                media_group.append(InputMediaPhoto(media=file_id, caption=msg.caption))
            else:
                obj_dict = msg.dict()
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
        for i in chats:
            await message.bot.send_media_group(i.id, media_group)
    else:
        for i in chats:
            await message.copy_to(i.id)
    await message.answer('Сообщение успешно отправлено!')
    await state.clear()
    await message.bot.delete_message(chat_id=message.from_user.id, message_id=message_id)


@router.callback_query(F.data == 'back')
async def back_to_menu(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.delete()
    await start_bot(call)
