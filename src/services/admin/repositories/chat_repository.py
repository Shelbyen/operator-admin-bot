from sqlalchemy import select
from sqlalchemy.orm import load_only

from ..models.chat_model import ChatModel
from .sqlalchemy_repository import SqlAlchemyRepository, ModelType
from src.config.database.db_helper import db_helper

from ..schemas.chat_schema import ChatCreate, ChatUpdate


class ChatRepository(SqlAlchemyRepository[ChatModel, ChatCreate, ChatUpdate]):
    async def filter(
            self,
            fields: list[str] | None = None,
            order: list[str] | None = None,
            limit: int = 100,
            offset: int = 0,
    ) -> list[ModelType] | None:
        async with self._session_factory() as session:
            stmt = select(self.model)
            if fields:
                model_fields = [getattr(self.model, field) for field in fields]
                stmt = stmt.options(load_only(*model_fields))
            if order:
                stmt = stmt.order_by(*order)
            if limit is not None:
                stmt = stmt.limit(limit)
            if offset is not None:
                stmt = stmt.offset(offset)

            row = await session.execute(stmt)
            return row.scalars().all()


chat_repository = ChatRepository(model=ChatModel, db_session=db_helper.get_db_session)
