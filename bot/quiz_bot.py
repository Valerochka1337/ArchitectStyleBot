from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import json

TOKEN = json.load(open("config.json"))["bot_token"]

storage = MemoryStorage()
dp = Dispatcher(storage=storage)
bot = Bot(TOKEN)