import asyncio

from aiogram import Dispatcher, Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from .config import TOKEN


bot = Bot(TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
loop = asyncio.get_event_loop()
dp = Dispatcher(bot, storage=storage, loop=loop)
