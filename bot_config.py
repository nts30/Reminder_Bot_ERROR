import asyncio
import logging

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.types import BotCommand

from database.sqlite_db import SQLiteDB
from handlers import reminder, other, bug_report
from config import load_config

storage = MemoryStorage()
logger = logging.getLogger(__name__)

config = load_config(r'config/config.ini')

TOKEN = config.tg_bot.BOT_TOKEN
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

DB = SQLiteDB()


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='/start', description='Начало работы'),
        BotCommand(command='/cancel', description='Отмена'),
        BotCommand(command='/bug_report', description='Отправить сообщение об ошибке'),
    ]

    await bot.set_my_commands(commands)


async def main():
    logging.info('Bot started')

    reminder(dp)

    await set_commands(bot=bot)
    await dp.start_polling(dp)


if __name__ == '__main__':
    logging.info('Bot started')

    reminder(dp)
    other(dp)
    bug_report(dp)

    asyncio.run(main())
