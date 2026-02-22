import asyncio

from app.di.di_container import DI

async def main():
    from app.bot.bot import run_bot

    await run_bot()


if __name__ == "__main__":
    asyncio.run(main())