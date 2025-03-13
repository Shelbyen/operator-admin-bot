from aiogram.filters import BaseFilter
from aiogram.types import Message


class ChatTypeFilter(BaseFilter):
    def __init__(self, is_group: bool = False, is_channel: bool = False):
        self.is_group = is_group
        self.is_channel = is_channel

    async def __call__(self, message: Message) -> bool:
        return (message.chat.type in ["group", "supergroup"]) == self.is_group or (message.chat.type == 'channel') == self.is_channel
