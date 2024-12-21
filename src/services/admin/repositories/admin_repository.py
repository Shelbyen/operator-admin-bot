from sqlalchemy import select
from sqlalchemy.orm import load_only

from src.config.database.db_helper import db_helper
from ..models.admin_model import AdminModel
from .sqlalchemy_repository import SqlAlchemyRepository, ModelType

from ..schemas.admin_schema import AdminCreate, AdminUpdate


class AdminRepository(SqlAlchemyRepository[AdminModel, AdminCreate, AdminUpdate]):
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

    async def all(self) -> list[ModelType] | None:
        return await self.filter()

    async def exists(self, **filters) -> bool:
        stmt = select(self.model).filter_by(**filters)
        async with self._session_factory() as session:
            result = await session.execute(stmt)
            return result.scalar() is not None


admin_repository = AdminRepository(model=AdminModel, db_session=db_helper.get_db_session)
