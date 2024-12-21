from typing import Callable, Dict, Any, Awaitable

from aiogram.types import TelegramObject, Message, CallbackQuery

from ..services.admin_service import admin_service


class PermissionMiddleware:
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        user = await admin_service.exists(str(event.from_user.id))
        if user:
            return await handler(event, data)
        return None
