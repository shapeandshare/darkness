import logging
import os

import click
import uvicorn
from fastapi import FastAPI

from ...api.common.routers import metrics
from .routers import chrono

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# pylint: disable=too-many-arguments,no-value-for-parameter
@click.command()
@click.option("--hostname", type=click.STRING, default="0.0.0.0", help="host address to bind to")
@click.option("--port", type=click.INT, default=9000, help="port to bind to")
@click.option("--log-level", type=click.STRING, default="INFO", help="log level (INFO, DEBUG, WARNING, ERROR, FATAL)")
@click.option("--darkness-hostname", type=click.STRING, default="0.0.0.0", help="state api address to connect to")
@click.option("--darkness-port", type=click.INT, default=9000, help="state api port to connect to")
@click.option("--darkness-sleep-time", type=click.FLOAT, default=1.0, help="state api call sleep time (seconds)")
@click.option("--darkness-timeout", type=click.FLOAT, default=5.0, help="state api call timeout (seconds)")
@click.option("--darkness-retries", type=click.INT, default=5, help="state api call retries (integer)")
@click.option(
    "--darkness-url", type=click.STRING, is_flag=False, default=None, help="state api url, format: '(host):(port)'"
)
def main(
    hostname: str,
    port: int,
    log_level: str,
    darkness_hostname: str,
    darkness_port: int,
    darkness_sleep_time: float,
    darkness_timeout: float,
    darkness_retries: int,
    darkness_url: str | None,
) -> None:
    logger.setLevel(logging.getLevelName(log_level))

    # Setup server runtime environment variables
    if darkness_url:
        os.environ["DARKNESS_TLD"] = darkness_url
    else:
        os.environ["DARKNESS_TLD"] = f"{darkness_hostname}:{darkness_port}"
    os.environ["DARKNESS_SERVICE_SLEEP_TIME"] = str(darkness_sleep_time)
    os.environ["DARKNESS_SERVICE_RETRY_COUNT"] = str(darkness_retries)
    os.environ["DARKNESS_SERVICE_TIMEOUT"] = str(darkness_timeout)

    logger.info("[Main] starting")
    app = FastAPI()

    logger.debug("[Main] adding metrics routes")
    app.include_router(metrics.router)

    logger.debug("[Main] adding Chrono routes")
    app.include_router(chrono.router)

    uvicorn.run(app, host=hostname, port=port, log_level=logging.getLevelName(log_level))
    logger.info("[Main] online")


if __name__ == "__main__":
    main()
