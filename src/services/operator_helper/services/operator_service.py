from .base_service import BaseService
from ..repositories.operator_repository import operator_repository
from ..repositories.sqlalchemy_repository import ModelType


class OperatorService(BaseService):
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

    async def exists(self, admin_id: str) -> bool:
        return await self.repository.exists(id=admin_id)


operator_service = OperatorService(repository=operator_repository)
