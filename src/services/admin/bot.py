import asyncio

from aiogram import Bot, Dispatcher

from config.project_config import settings
from handlers import admin
from middlewares.permission_middleware import PermissionMiddleware
from services.admin_service import admin_service
from aiogram.types import BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = []
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def on_startup(bot: Bot):
    admins = dir(settings)[:4]
    admins.pop(admins.index('TOKEN'))
    for ad in admins:
        pk = getattr(settings, ad)
        if not await admin_service.exists(pk):
            await admin_service.fast_create(pk)
    await set_commands(bot)
    print('Бот вышел в онлайн')


async def main():
    bot = Bot(token=settings.TOKEN)
    dp = Dispatcher()

    admin.router.message.middleware(PermissionMiddleware())

    dp.include_routers(admin.router)

    dp.startup.register(on_startup)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
