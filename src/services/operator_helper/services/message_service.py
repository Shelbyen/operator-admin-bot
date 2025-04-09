from typing import List

from .base_service import BaseService
from ..repositories.message_repository import message_repository
from ..schemas.message_schema import MessageCreate, MessageBase


class MessageService(BaseService):
    async def create_many(self, messages: List[MessageCreate]) -> None:
        if len(messages) != 0:
            await self.repository.create_many(messages)

    async def get_by_chat(self, chat_id: str) -> list[MessageBase] | None:
        return await self.repository.get_by_chat(chat_id=chat_id)


message_service = MessageService(repository=message_repository)
