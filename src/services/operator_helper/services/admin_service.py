from datetime import datetime

from .base_service import BaseService
from repositories.admin_repository import admin_repository


class AdminService(BaseService):
    async def check_invite(self, invite_hash: int) -> bool:
        admin = await self.repository.find_hash(invite_hash)
        if admin is None:
            return False
        return admin.invite_date >= datetime.now()


admin_service = AdminService(repository=admin_repository)
