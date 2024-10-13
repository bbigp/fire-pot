import asyncio
import random

from fastapi import FastAPI

from lib.router import request_mapping
from lib.utils import logger


def create_app():
    app = FastAPI(debug=True, title="RSS Hub")
    app.include_router(request_mapping)

    # logger.info("🎉 RSSHub is running on port 1210! Cheers!")
    # logger.info("💖 Can you help keep this open source project alive? Please sponsor 👉 https://docs.rsshub.app/sponsor")
    # logger.info("🔗 Local: 👉 http://localhost:1210")
    logger.info("RSSHub is running on port 1210! Cheers!")
    logger.info("Can you help keep this open source project alive? Please sponsor https://docs.rsshub.app/sponsor")
    logger.info("Local: http://localhost:1210")
    return app


app = create_app()


@app.on_event("startup")
def on_startup():
    asyncio.create_task(fetch_task())

details_queue = asyncio.Queue()

async def fetch_task():
    logger.info('background task start..')
    while True:
        if details_queue.empty():
            await asyncio.sleep(2)
        else:
            back_task = await details_queue.get()
            back_task.route.content_handler(back_task.link)
            sleep_time = random.uniform(2, 20)
            logger.info(f'sleep time: {sleep_time}')
            await asyncio.sleep(sleep_time)