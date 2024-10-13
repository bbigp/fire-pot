import asyncio

from fastapi import FastAPI

from lib.cron import fetch_task
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



