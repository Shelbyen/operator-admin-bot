from .base_service import BaseService
from ..repositories.chat_repository import chat_repository
from ..repositories.sqlalchemy_repository import ModelType


class ChatService(BaseService):
    async def filter(
            self,
            fields: list[str] | None = None,
            order: list[str] | None = None,
            limit: int | None = None,
            offset: int | None = None
    ) -> list[ModelType] | None:
        return await self.repository.filter(
            fields=fields,
            order=order,
            limit=limit,
            offset=offset
        )


chat_service = ChatService(repository=chat_repository)
