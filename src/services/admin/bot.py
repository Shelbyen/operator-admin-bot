import asyncio

from aiogram import Bot, Dispatcher

from config.project_config import settings
from handlers import admin
from middlewares.permission_middleware import PermissionMiddleware
from services.admin_service import admin_service
from middlewares.log_middleware import LogMiddleware


async def set_commands(bot: Bot):
    await bot.delete_my_commands()


async def check_admin_list():
    admins = settings.ADMINS.split('/')
    for ad in admins:
        if not await admin_service.exists(ad):
            await admin_service.fast_create(ad)


async def on_startup(bot: Bot):
    await check_admin_list()
    await set_commands(bot)
    print('Бот вышел в онлайн')


async def main():
    bot = Bot(token=settings.TOKEN)
    dp = Dispatcher()
    dp.callback_query.outer_middleware(LogMiddleware())
    dp.message.outer_middleware(LogMiddleware())
    admin.router.message.middleware(PermissionMiddleware())

    dp.include_routers(admin.router)

    dp.startup.register(on_startup)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
