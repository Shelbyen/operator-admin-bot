from .base_service import BaseService
from ..repositories.message_repository import message_repository
from ..repositories.sqlalchemy_repository import ModelType


class MessageService(BaseService):
    async def get_by_phone(self, phone: str, chat_id: str) -> ModelType | None:
        return await self.repository.get_by_phone(phone=phone, chat_id=chat_id)

    async def get_by_chat(self, chat_id: str) -> list[ModelType] | None:
        return await self.repository.get_by_chat(chat_id=chat_id)


message_service = MessageService(repository=message_repository)
