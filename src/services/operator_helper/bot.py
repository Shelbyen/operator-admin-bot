import asyncio

from aiogram import Bot, Dispatcher

from config.project_config import settings
from handlers import operator, user_register, group_register
from middlewares.album_middleware import AlbumMiddleware
from middlewares.permission_middleware import PermissionMiddleware


async def on_startup():
    print('Бот вышел в онлайн')


async def main():
    bot = Bot(token=settings.TOKEN)
    dp = Dispatcher()

    dp.message.outer_middleware(AlbumMiddleware())
    user_register.router.message.middleware(PermissionMiddleware(is_operator=False))
    operator.router.message.middleware(PermissionMiddleware())
    group_register.router.message.middleware(PermissionMiddleware())

    dp.include_routers(user_register.router, operator.router, group_register.router)

    dp.startup.register(on_startup)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
