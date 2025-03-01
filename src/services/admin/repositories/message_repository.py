from sqlalchemy import select

from src.config.database.db_helper import db_helper
from .sqlalchemy_repository import SqlAlchemyRepository, ModelType
from ..models.message_model import MessageModel
from ..schemas.message_schema import MessageCreate, MessageUpdate


class MessageRepository(SqlAlchemyRepository[MessageModel, MessageCreate, MessageUpdate]):
    async def get_by_phone(
            self,
            phone: str,
            chat_id: str
    ) -> ModelType | None:
        async with self._session_factory() as session:
            stmt = select(self.model).where(self.model.phone == phone, self.model.chat_id == chat_id).order_by(
                self.model.created_at)

            row = await session.execute(stmt)
            return row.scalars().first()

    async def get_by_chat(self, chat_id: str) -> list[ModelType] | None:
        async with self._session_factory() as session:
            stmt = select(self.model).where(self.model.chat_id == chat_id).order_by(self.model.created_at)

            row = await session.execute(stmt)
            return row.scalars().all()


message_repository = MessageRepository(model=MessageModel, db_session=db_helper.get_db_session)
