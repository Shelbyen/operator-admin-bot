import asyncio

from aiogram import Dispatcher
from fastapi import FastAPI, HTTPException, Header, Depends
import uvicorn

from src.services.admin.bot import admin_bot
from src.services.admin.middlewares.album_middleware import AlbumMiddleware
from src.services.admin.middlewares.log_middleware import LogMiddleware
from src.services.operator_helper.bot import operator_bot
from src.config.project_config import settings

app = FastAPI(title="OperatorBot API")

async def verify_bearer_token(authorization: str | None = Header(None)):
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")

    token = authorization.split(" ")[1]
    if token != settings.SERVICE_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.get("/send_photo")
async def send_photo(
    group_id: int,
    file_id: str,
    token: None = Depends(verify_bearer_token) # pylint: disable=unused-argument
):
    bot = operator_bot.bot

    message = await bot.send_photo(chat_id=group_id, photo=file_id)
    return {"status": "ok", "message_url": message.get_url()}


async def run_fastapi():
    config = uvicorn.Config(
        app, host="127.0.0.1", port=settings.SERVICE_PORT, loop="asyncio", log_level="info"
    )
    server = uvicorn.Server(config)
    await server.serve()


async def start_bots_polling():
    dp = Dispatcher()

    dp.message.outer_middleware(AlbumMiddleware())
    dp.message.outer_middleware(LogMiddleware())
    dp.callback_query.outer_middleware(LogMiddleware())

    await admin_bot.start_bot(dp)
    await operator_bot.start_bot(dp)

    loop = asyncio.get_running_loop()
    loop.create_task(run_fastapi())

    await dp.start_polling(operator_bot.bot, admin_bot.bot)


if __name__ == '__main__':
    asyncio.run(start_bots_polling())
