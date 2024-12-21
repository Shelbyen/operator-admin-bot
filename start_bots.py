import asyncio

from aiogram import Dispatcher

from src.config.project_config import settings
from src.services.admin.bot import admin_bot
from src.services.admin.middlewares.album_middleware import AlbumMiddleware
from src.services.admin.middlewares.log_middleware import LogMiddleware
from src.services.operator_helper.bot import operator_bot


async def start_bots_polling():
    dp = Dispatcher()

    dp.message.outer_middleware(AlbumMiddleware())
    dp.message.outer_middleware(LogMiddleware())
    dp.callback_query.outer_middleware(LogMiddleware())

    await admin_bot.start_bot(dp)
    await operator_bot.start_bot(dp)

    await dp.start_polling(operator_bot.bot, admin_bot.bot)


if __name__ == '__main__':
    asyncio.run(start_bots_polling())
