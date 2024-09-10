from aiogram.filters import BaseFilter
from aiogram.types import Message


class ChatTypeFilter(BaseFilter):
    def __init__(self, is_group: bool = False):
        self.is_group = is_group

    async def __call__(self, message: Message) -> bool:
        return (message.chat.type in ["group", "supergroup"]) == self.is_group
