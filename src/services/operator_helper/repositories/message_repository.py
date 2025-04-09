from sqlalchemy import insert, select
from typing import List

from ..models.message_model import MessageModel
from .sqlalchemy_repository import SqlAlchemyRepository, ModelType
from src.config.database.db_helper import db_helper

from ..schemas.message_schema import MessageCreate, MessageUpdate


class MessageRepository(SqlAlchemyRepository[MessageModel, MessageCreate, MessageUpdate]):
    async def create_many(self, messages: List[MessageCreate]) -> None:
        async with self._session_factory() as session:
            await session.execute(
                insert(self.model),
                messages,
            )
            await session.commit()

    async def get_by_chat(self, chat_id: str) -> list[ModelType] | None:
        async with self._session_factory() as session:
            stmt = select(self.model).where(self.model.chat_id == chat_id).order_by(self.model.created_at)

            row = await session.execute(stmt)
            return row.scalars().all()



message_repository = MessageRepository(model=MessageModel, db_session=db_helper.get_db_session)
