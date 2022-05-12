from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage=MemoryStorage()

# bot = Bot(token=os.getenv('TOKEN'))
bot = Bot(token=('5136198355:AAGwHHpaOi6vuMPF8eyczIGhQJJQ9W7ZYQU'))
dp = Dispatcher(bot, storage=storage)