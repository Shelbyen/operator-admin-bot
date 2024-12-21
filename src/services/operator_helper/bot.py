from aiogram import Bot, Dispatcher

from .handlers import operator, user_register, group_register
from .middlewares.permission_middleware import PermissionMiddleware
from src.config.project_config import settings


async def on_startup():
    print('Бот вышел в онлайн')


class OperatorBot:
    def __init__(self):
        self.bot = Bot(token=settings.OPERATOR_TOKEN)

    def register_dispatcher(self, dp: Dispatcher):
        user_register.router.message.middleware(PermissionMiddleware(is_operator=False))
        operator.router.message.middleware(PermissionMiddleware())
        group_register.router.message.middleware(PermissionMiddleware())

        dp.include_routers(user_register.router, operator.router, group_register.router)

        dp.startup.register(on_startup)

    async def start_bot(self, dp: Dispatcher):
        self.register_dispatcher(dp)
        await self.bot.delete_webhook(drop_pending_updates=True)

operator_bot = OperatorBot()
