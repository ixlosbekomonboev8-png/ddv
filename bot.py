import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import router
from aiohttp import web

# Loglarni sozlash
logging.basicConfig(level=logging.INFO)

# Render uchun Health Check serveri
async def handle(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    # Render PORT environment variable'ni avtomatik beradi, bo'lmasa 10000 dan foydalanadi
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logging.info(f"Health check server started on port {port}")

async def main():
    if TOKEN == "BOT_TOKENINI_SHU_YERGA_YOZING":
        logging.error("Xatolik: Iltimos, config.py fayliga bot tokenini kiriting!")
        return

    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    
    # Bot va Veb-serverni parallel ravishda ishga tushiramiz
    await asyncio.gather(
        start_web_server(),
        dp.start_polling(bot)
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot to'xtatildi.")
