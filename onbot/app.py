from loguru import logger
from aiogram import executor, Dispatcher
from tortoise import Tortoise

from onbot.core.config import DB_URL, ADMIN


async def db_init():
    await Tortoise.init(
        db_url=DB_URL,
        modules={
            'models': ["onbot.models"]
        },
    )
    await Tortoise.generate_schemas()
    logger.info("Database inited")


async def on_startup(dp: Dispatcher):
    await dp.bot.send_message(ADMIN, "Bot started")


async def on_shutdown(dp: Dispatcher):
    try:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await Tortoise.close_connections()
    except Exception as e:
        logger.error(e)


if __name__ == '__main__':
    from onbot.handlers import dp
    dp.loop.create_task(db_init())
    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown
    )