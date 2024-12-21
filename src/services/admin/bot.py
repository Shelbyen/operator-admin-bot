from aiogram import Bot, Dispatcher

from .handlers import admin
from .middlewares.permission_middleware import PermissionMiddleware
from .services.admin_service import admin_service
from src.config.project_config import settings


async def set_commands(bot):
    await bot.delete_my_commands()


async def check_admin_list():
    admins = settings.ADMINS.split('/')
    for ad in admins:
        if not await admin_service.exists(ad):
            await admin_service.fast_create(ad)


async def on_startup(bot):
    await check_admin_list()
    await set_commands(bot)
    print('Админ вышел в онлайн')


class AdminBot:
    def __init__(self):
        self.bot = Bot(token=settings.ADMIN_TOKEN)

    def register_dispatcher(self, dp: Dispatcher):
        admin.router.message.middleware(PermissionMiddleware())

        dp.include_routers(admin.router)

        dp.startup.register(on_startup)

    async def start_bot(self, dp: Dispatcher):
        self.register_dispatcher(dp)
        await check_admin_list()
        await self.bot.delete_webhook(drop_pending_updates=True)


admin_bot = AdminBot()
