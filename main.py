from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from lib.config import logger
from lib.router import request_mapping


def create_app():
    app = FastAPI(debug=True, title="RSS Hub")
    app.include_router(request_mapping)

    print("RSSHub is running on port 1210")
    # logger.info("🎉 RSSHub is running on port 1210! Cheers!")
    # logger.info("💖 Can you help keep this open source project alive? Please sponsor 👉 https://docs.rsshub.app/sponsor")
    # logger.info("🔗 Local: 👉 http://localhost:1210")
    return app


app = create_app()