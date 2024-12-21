from aiogram.filters import BaseFilter
from aiogram.types import Message


class BotFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.bot.id == 7906656739
