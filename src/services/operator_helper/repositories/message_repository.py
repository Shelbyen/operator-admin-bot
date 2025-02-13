from sqlalchemy import insert
from typing import List

from ..models.message_model import MessageModel
from .sqlalchemy_repository import SqlAlchemyRepository
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


message_repository = MessageRepository(model=MessageModel, db_session=db_helper.get_db_session)
