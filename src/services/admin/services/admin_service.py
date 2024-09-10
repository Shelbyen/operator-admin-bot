from datetime import datetime, timedelta
from random import randint

from repositories.sqlalchemy_repository import ModelType
from .base_service import BaseService
from repositories.admin_repository import admin_repository
from schemas.admin_schema import AdminUpdate, AdminCreate


class AdminService(BaseService):

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

    async def exists(self, admin_id: int) -> bool:
        return await self.repository.exists(id=admin_id)

    async def get_with_update(self, admin_id: int) -> ModelType | None:
        admin = await self.repository.get_single(id=admin_id)
        if admin is None:
            return
        if admin.invite_date < datetime.now():
            admin.invite_date = datetime.now() + timedelta(minutes=15)
            admin.invite_hash = hash(admin.id + randint(10000, 10000000))
            await self.update(admin_id, AdminUpdate(invite_hash=admin.invite_hash, invite_date=admin.invite_date))
        return admin

    async def check_invite(self, pk: int, invite_hash: int) -> bool:
        admin = await self.repository.get_single(id=pk)
        if admin is None:
            return False
        return admin.invite_hash == invite_hash and admin.invite_date >= datetime.now()

    async def fast_create(self, pk: int) -> ModelType:
        return await self.create(AdminCreate(id=pk, invite_hash=hash(pk + randint(10000, 10000000))))


admin_service = AdminService(repository=admin_repository)
