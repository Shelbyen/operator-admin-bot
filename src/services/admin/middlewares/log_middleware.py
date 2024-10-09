from datetime import datetime
from typing import Callable, Dict, Any, Awaitable

from aiogram.types import TelegramObject, Message, CallbackQuery


class LogMiddleware:
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        text_data = type(event)
        if type(event) == Message:
            text_data = event.text
        if type(event) == CallbackQuery:
            text_data = event.data
        print(datetime.now(), " From: ", event.from_user.id, " ", event.from_user.username, " Text data: ", text_data)
        return await handler(event, data)
