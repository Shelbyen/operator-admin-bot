from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message
from aiogram.exceptions import TelegramBadRequest


class ChatExistFilter(BaseFilter):
    def __init__(self, get_chat_id_func, entity: str = 'call'):
        self.get_chat_id = get_chat_id_func
        self.entity_for_find = entity
    async def __call__(self,
                       message: Message | None = None,
                       call: CallbackQuery | None = None) -> bool:
        entity = (message, call)[self.entity_for_find == 'call']
        if entity is None:
            return False
        try:
            await bot.get_chat(
                chat_id=self.get_chat_id(self.get_chat_id(entity))
            )
        except TelegramBadRequest as e:
            if "chat not found" not in str(e).lower():
                print(e)
                return False
            if isinstance(entity, Message):
                await entity.answer(
                    'Сохранен неправильный чат, удалите и добавьте бота заного!')
            else:
                await entity.bot.send_message(
                    chat_id=entity.from_user.id,
                    text='Сохранен неправильный чат, удалите и добавьте бота заного!')
            return False
        return True
