import os
import logging

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from app.bot.handlers import router as tasks_router

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def run_bot():
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
