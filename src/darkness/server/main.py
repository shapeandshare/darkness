import logging

import uvicorn
from fastapi import FastAPI

from .routers import island

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


if __name__ == "__main__":

    logger.info("[Main] starting")
    app = FastAPI()

    logger.debug("[Main] adding island routes")
    app.include_router(island.router)

    logger.info("[Main] online")

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level=logging.getLogger().level)
