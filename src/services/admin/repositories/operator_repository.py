from sqlalchemy import select
from sqlalchemy.orm import load_only

from models.operator_model import OperatorModel
from .sqlalchemy_repository import SqlAlchemyRepository, ModelType
from config.database.db_helper import db_helper

from schemas.operator_schema import OperatorCreate, OperatorUpdate


class OperatorRepository(SqlAlchemyRepository[OperatorModel, OperatorCreate, OperatorUpdate]):
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


operator_repository = OperatorRepository(model=OperatorModel, db_session=db_helper.get_db_session)
