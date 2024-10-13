import asyncio
import random

from lib.utils import logger

details_queue = asyncio.Queue()

async def fetch_task():
    logger.info('[cron]background task start..')
    while True:
        if details_queue.empty():
            await asyncio.sleep(2)
        else:
            logger.info('[cron]background task doing..')
            back_task = await details_queue.get()
            back_task.execute()
            sleep_time = random.uniform(2, 20)
            logger.info(f'[cron]sleep {sleep_time}')
            await asyncio.sleep(sleep_time)