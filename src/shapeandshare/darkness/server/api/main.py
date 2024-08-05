import logging
import os

import click
import uvicorn
from fastapi import FastAPI

from .routers import island, islands, metrics

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


@click.command()
@click.option("--hostname", type=click.STRING, default="0.0.0.0", help="host address to bind to")
@click.option("--port", type=click.INT, default=8000, help="port to bind to")
@click.option("--log-level", type=click.STRING, default="INFO", help="log level (INFO, DEBUG, WARNING, ERROR, FATAL)")
@click.option("--sleep-time", type=click.FLOAT, default=1.0, help="api call sleep time (seconds)")
@click.option("--timeout", type=click.FLOAT, default=5.0, help="api call timeout (seconds)")
@click.option("--retries", type=click.INT, default=5, help="api call retries (integer)")
@click.option("--url", type=click.STRING, is_flag=False, default=None, help="darkness api url, format: '(host):(port)'")
def main(
    hostname: str, port: int, log_level: str, sleep_time: float, timeout: float, retries: int, url: str | None
) -> None:
    logger.setLevel(logging.getLevelName(log_level))

    # Setup server runtime environment variables
    if url:
        os.environ["DARKNESS_TLD"] = url
    else:
        os.environ["DARKNESS_TLD"] = f"{hostname}:{port}"
    os.environ["DARKNESS_SERVICE_SLEEP_TIME"] = str(sleep_time)
    os.environ["DARKNESS_SERVICE_RETRY_COUNT"] = str(retries)
    os.environ["DARKNESS_SERVICE_TIMEOUT"] = str(timeout)

    logger.info("[Main] starting")
    app = FastAPI()

    logger.debug("[Main] adding metrics routes")
    app.include_router(metrics.router)

    logger.debug("[Main] adding island routes")
    app.include_router(island.router)

    logger.debug("[Main] adding islands routes")
    app.include_router(islands.router)

    logger.info("[Main] online")

    uvicorn.run(app, host=hostname, port=port, log_level=logging.getLevelName(log_level))


if __name__ == "__main__":
    main()
