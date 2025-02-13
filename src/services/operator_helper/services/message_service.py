from typing import List

from .base_service import BaseService
from ..repositories.message_repository import message_repository
from ..schemas.message_schema import MessageCreate


class MessageService(BaseService):
    async def create_many(self, messages: List[MessageCreate]) -> None:
        if len(messages) != 0:
            await self.repository.create_many(messages)


message_service = MessageService(repository=message_repository)
