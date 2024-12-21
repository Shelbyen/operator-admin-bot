from sqlalchemy import select

from ..models.admin_model import AdminModel
from .sqlalchemy_repository import SqlAlchemyRepository, ModelType
from src.config.database.db_helper import db_helper

from ..schemas.admin_schema import AdminCreate, AdminUpdate


class AdminRepository(SqlAlchemyRepository[AdminModel, AdminCreate, AdminUpdate]):
    async def find_hash(self, invite_hash: int) -> ModelType | None:
        async with self._session_factory() as session:
            stmt = select(self.model).where(AdminModel.invite_hash == invite_hash)

            row = await session.execute(stmt)
            return row.scalars().first()

    async def exists(self, **filters) -> bool:
        stmt = select(self.model).filter_by(**filters)
        async with self._session_factory() as session:
            result = await session.execute(stmt)
            return result.scalar() is not None


admin_repository = AdminRepository(model=AdminModel, db_session=db_helper.get_db_session)
