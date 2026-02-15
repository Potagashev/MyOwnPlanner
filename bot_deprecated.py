import os
import asyncio
import logging

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router
from database import init_db
from di.di_container import DI

from bot.handlers import router as tasks_router

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


di = DI()
di.init()



async def main():
    load_dotenv()

    BOT_TOKEN = os.getenv('BOT_TOKEN')

    if not BOT_TOKEN:
        logger.error("ОШИБКА: Не найден BOT_TOKEN в файле .env")
        exit(1)

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(tasks_router)

    logger.info("Бот запускается...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())