import asyncio
import aioschedule

from bot_config import bot, DB


async def send_reminder():
    all_info = DB.send_remind()
    if all_info is not None:
        for remind in all_info:
            await bot.send_message(remind.user_id, f'{remind.name}, напоминаю:\n\n{remind.text}')


async def scheduler():
    aioschedule.every(1).minute.do(send_reminder)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
