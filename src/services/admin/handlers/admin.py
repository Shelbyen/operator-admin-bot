import re
from typing import Optional, List

from aiogram import Router, F
from aiogram.exceptions import TelegramMigrateToChat, TelegramForbiddenError, TelegramBadRequest
from aiogram.exceptions import TelegramNotFound
from aiogram.filters import Command, BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, InputMediaDocument, InputMediaVideo, InputMediaAudio, \
    InputMediaAnimation
from aiogram.utils.deep_linking import create_deep_link

from src.config.project_config import settings
from src.services.operator_helper.bot import operator_bot
from src.use_cases.chat_keyboard_use_case import get_chat_keyboards
from ..filters.chat_type import ChatTypeFilter
from ..filters.is_admin_bot import BotFilter
from ..keyboards.admin_kb import create_admin_choosing, create_menu, back_button, deleting_messages_kb
from ..schemas.chat_schema import ChatBase, ChatCreate
from ..schemas.message_schema import MessageBase
from ..services.admin_service import admin_service
from ..services.chat_service import chat_service
from ..services.message_service import message_service
from ..services.operator_service import operator_service

router = Router()
router.message.filter(ChatTypeFilter())
router.message.filter(BotFilter())
router.callback_query.filter(BotFilter())


class IsSuperAdmin(BaseFilter):
    def __init__(self):
        self.super_admins = settings.ADMINS_1.split('/')

    async def __call__(self, message: Message) -> bool:
        return str(message.from_user.id) in self.super_admins

    def fast_check(self, check_id: int) -> bool:
        return str(check_id) in self.super_admins


class SendMessageToAll(StatesGroup):
    write_text = State()


class MessageDeleting(StatesGroup):
    choosing_chat = State()
    choosing_number = State()


def chunks(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]


async def fix_deleting_message(target_message: MessageBase):
    if target_message:
        try:
            await operator_bot.bot.delete_message(target_message.chat_id, target_message.id)
            await message_service.delete(pk=target_message.id)
        except TelegramNotFound or TelegramBadRequest:
            return 'Сообщение уже удалено'
        else:
            return 'Сообщение успешно удалено!'
    else:
        return 'Сообщение не найдено'


def except_when_send(send_function):
    async def wrapper(chat: ChatBase, *args, **kwargs):
        try:
            await send_function(chat, *args, **kwargs)
        except TelegramMigrateToChat as e:
            await chat_service.delete(chat.id)
            await chat_service.create(ChatCreate(id=e.migrate_to_chat_id, name=chat.name))
            chat.id = e.migrate_to_chat_id
            await send_function(chat, *args, **kwargs)

    return wrapper


@except_when_send
async def fix_send_media_group(chat: ChatBase, media_group):
    await operator_bot.bot.send_media_group(chat.id, media_group)


@except_when_send
async def fix_send_message(chat: ChatBase, message):
    await operator_bot.bot.send_message(chat.id, message)


start_message = "**Добавить чаты** - по нажатию на кнопку бот дает ссылку на добавления чатов, при нажатии на нее автоматически откроется меню TG с выбором чатов. После выбора чата необходимо просто нажат на кнопку 'Добавить бота' не добавляю ему каких либо привилегий. После добавления бот должен написать в чат 'Чат успешно добавлен'.\n\n**Удалить чаты** - по нажатию на кнопку выпадет меню со всеми подключенными чатами. При нажатии на чат он автоматически удалится.\n\n**Добавить операторов** - по нажатию выдаст ссылку-приглашение. Срок действия ссылки - 15 минут, после этого необходимо снова создать ссылку.\n\n**Удалить операторов** - по нажатию выпадает меню со всеми операторами. При нажатии удаляет оператора.\n"


@router.message(Command('update'))
async def update_keyboard(message: Message):
    admins = await admin_service.filter()
    new_keyboard_1 = create_menu(True)
    new_keyboard_2 = create_menu()
    admins_1 = settings.ADMINS_1.split('/')
    for admin in admins:
        try:
            await message.bot.send_message(admin.id, 'Сообщение для обновления клавиатуры',
                                           reply_markup=new_keyboard_1 if admin.id in admins_1 else new_keyboard_2)
        except TelegramForbiddenError:
            continue
        except TelegramBadRequest:
            print('Чат не найден с', admin.id)
    await message.answer('Клавиатура обновлена!')


@router.message(Command('start'))
async def start_bot(message: Message | CallbackQuery):
    await message.bot.send_message(message.from_user.id, start_message, parse_mode="Markdown",
                                   reply_markup=create_menu(IsSuperAdmin().fast_check(message.from_user.id)))


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
    chats = await chat_service.filter(limit=450, order=['name'])
    for kb in get_chat_keyboards(chats, '2'):
        await message.answer("Выберите чаты которые хотите удалить:",
                             reply_markup=kb)


@router.callback_query(F.data[0] == '2')
async def delete_chat(call: CallbackQuery):
    chat_id = int(call.data.split('|')[1])
    if await chat_service.get(str(chat_id)):
        await chat_service.delete(str(chat_id))
        await operator_bot.bot.leave_chat(chat_id=chat_id)

    await choosing_delete_chat_start(call.message)


@router.message(F.text.lower() == "удалить операторов")
async def choosing_delete_admin_start(message: Message):
    await message.answer("Выберите операторов которых хотите удалить:",
                         reply_markup=await create_admin_choosing())


@router.callback_query(F.data[0] == '1')
async def delete_admin(call: CallbackQuery):
    operator_id = call.data.split('|')[1]

    await operator_service.delete(operator_id)
    await choosing_delete_admin_start(call.message)


@router.message(F.text.lower() == "отправить во все чаты", IsSuperAdmin())
async def send_all_command(message: Message, state: FSMContext):
    await state.set_state(SendMessageToAll.write_text)
    message = await message.answer(f"Отправьте ваше сообщение", reply_markup=back_button())
    await state.update_data({'message_id': message.message_id})


@router.message(SendMessageToAll.write_text)
async def mass_mailing(message: Message, state: FSMContext, album: Optional[List[Message]] = None):
    message_id = (await state.get_data())['message_id']
    chats: List[ChatBase] = await chat_service.filter(limit=500)
    send = {}
    if album:
        media_group = []
        for msg in album:
            if msg.photo:
                file_id = msg.photo[-1].file_id
                media_group.append(InputMediaPhoto(media=file_id, caption=msg.caption))
                send.setdefault('photo', []).append((file_id, msg.caption))
            else:
                obj_dict = msg.model_dump()
                file_id = obj_dict[msg.content_type]['file_id']
                send.setdefault(msg.content_type, []).append((file_id, msg.caption))
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
            await fix_send_media_group(i, media_group)

    else:
        for i in chats:
            await fix_send_message(i, message.text)

    await message.answer('Сообщение успешно отправлено!')
    await state.clear()
    await message.bot.delete_message(chat_id=message.from_user.id, message_id=message_id)


@router.message(F.text.lower() == 'удалить сообщение')
async def delete_message_command(data: Message | CallbackQuery, state: FSMContext):
    chats = await chat_service.filter(limit=450, order=['name'])

    # TODO: CHANGE THIS SHIT

    true_chats = [chat for chat in chats if await message_service.get_by_chat(chat.id)]

    messages = []
    for kb in get_chat_keyboards(true_chats, '3'):
        if type(data) is Message:
            msg = await data.answer("Выберите группу", reply_markup=kb)
        else:
            msg = await data.message.answer("Выберите группу", reply_markup=kb)
        messages.append(msg.message_id)

    await state.update_data({'messages_id': messages})
    await state.set_state(MessageDeleting.choosing_chat)


@router.callback_query(F.data[0] == '3', MessageDeleting.choosing_chat)
async def get_chat_for_message(call: CallbackQuery, state: FSMContext):
    chat = await chat_service.get(call.data.split('|')[1])
    state_data = await state.get_data()
    messages = state_data['messages_id']
    await state.update_data({'chat_id': int(call.data.split('|')[1])})
    for i in messages:
        await call.bot.delete_message(call.from_user.id, i)

    messages = await message_service.get_by_chat(chat_id=chat.id)
    msg = await call.message.answer(
        f"Выбранный чат: {chat.name}\nТеперь выберите из списка или отправьте сообщением нужный номер",
        reply_markup=deleting_messages_kb(messages))
    await state.update_data({'message_id': msg.message_id, 'chat_id': chat.id})
    await state.set_state(MessageDeleting.choosing_number)


@router.callback_query(F.data[0] == '5', MessageDeleting.choosing_number)
async def return_to_chat_choosing(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.set_data({})
    await state.set_state(MessageDeleting.choosing_chat)
    await delete_message_command(call, state)


@router.callback_query(F.data[0] == '4', MessageDeleting.choosing_number)
async def delete_message(call: CallbackQuery, state: FSMContext):
    chat_id = (await state.get_data())['chat_id']
    target_message: MessageBase = await message_service.get_by_phone(chat_id=chat_id,
                                                                     phone=call.data.split('|')[1])
    await call.message.answer(await fix_deleting_message(target_message))
    await call.message.delete()


@router.message(MessageDeleting.choosing_number)
async def delete_message(message: Message, state: FSMContext):
    state_data = await state.get_data()

    if not message.text:
        await message.answer('Введите телефон правильно!')
        return

    numbers = [i[0] for i in re.finditer(r'((\+7|8|7)[\- ]?)[0-9]{10}', message.text)]
    if len(numbers) == 0:
        await message.answer('Введите телефон правильно!')
        return
    target_number = numbers[0][-10:]

    target_message: MessageBase = await message_service.get_by_phone(chat_id=str(state_data['chat_id']), phone=target_number)

    await message.answer(await fix_deleting_message(target_message))

    await state.clear()
    await message.bot.delete_message(chat_id=message.from_user.id, message_id=state_data['message_id'])

    await delete_message_command(message, state)


@router.callback_query(F.data == 'back')
async def back_to_menu(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.delete()
