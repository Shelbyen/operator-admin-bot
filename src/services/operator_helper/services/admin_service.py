from datetime import datetime

from .base_service import BaseService
from repositories.admin_repository import admin_repository


class AdminService(BaseService):
    async def check_invite(self, invite_hash: int) -> bool:
        admin = await self.repository.find_hash(invite_hash)
        return admin is not None

    async def exists(self, admin_id: str) -> bool:
        return await self.repository.exists(id=admin_id)


admin_service = AdminService(repository=admin_repository)
