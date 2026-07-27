import asyncio
import logging
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from aiohttp import web
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from services.db import init_db

from handlers.start import router as start_router
from handlers.generate import router as generate_router
from handlers.styles import router as styles_router
from handlers.premium import router as premium_router


async def health_handler(request):
    return web.json_response({"status": "ok"})


async def start_http_server():
    port = int(os.environ.get("PORT", 10000))
    app = web.Application()
    app.router.add_get("/", health_handler)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"HTTP-сервер запущен на порту {port}")


async def main():
    logging.basicConfig(level=logging.INFO)
    await init_db()

    await start_http_server()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(styles_router)
    dp.include_router(premium_router)
    dp.include_router(generate_router)

    print("Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
