import logging
import os

import click
import uvicorn
from fastapi import FastAPI

from ..common.routers import metrics

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# pylint: disable=too-many-arguments,no-value-for-parameter
@click.command()
@click.option("--hostname", type=click.STRING, default="0.0.0.0", help="monogdb host address to connect to")
@click.option("--port", type=click.INT, default=8000, help="monogdb host port to connect to")
@click.option("--mongodb-hostname", type=click.STRING, default="0.0.0.0", help="monogdb host address to connect to")
@click.option("--mongodb-port", type=click.INT, default=27017, help="monogdb host port to connect to")
@click.option("--mongodb-database", type=click.STRING, default="darkness", help="monogdb database name")
@click.option("--log-level", type=click.STRING, default="INFO", help="log level (INFO, DEBUG, WARNING, ERROR, FATAL)")
def main(
    hostname: str, port: int, mongodb_hostname: str, mongodb_port: int, mongodb_database: str, log_level: str
) -> None:
    logger.setLevel(logging.getLevelName(log_level))

    os.environ["DARKNESS_MONGODB_HOST"] = mongodb_hostname
    os.environ["DARKNESS_MONGODB_PORT"] = str(mongodb_port)
    os.environ["DARKNESS_MONGODB_DATABASE"] = mongodb_database

    # these much import after the above env vars are set
    from .routers import world, worlds

    logger.info("[Main] starting")
    app = FastAPI()

    logger.debug("[Main] adding metrics routes")
    app.include_router(metrics.router)

    logger.debug("[Main] adding world routes")
    app.include_router(world.router)

    logger.debug("[Main] adding worlds routes")
    app.include_router(worlds.router)

    logger.info("[Main] online")

    uvicorn.run(app, host=hostname, port=port, log_level=logging.getLevelName(log_level))


if __name__ == "__main__":
    main()
