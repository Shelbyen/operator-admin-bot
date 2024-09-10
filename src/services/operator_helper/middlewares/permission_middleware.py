from typing import Callable, Dict, Any, Awaitable

from aiogram.types import TelegramObject, Message, CallbackQuery

from services.operator_service import operator_service


class PermissionMiddleware:
    def __init__(self, is_operator=True):
        self.is_operator = is_operator

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        user = await operator_service.exists(event.from_user.id)
        if user == self.is_operator:
            return await handler(event, data)
        return None
