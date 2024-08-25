import logging
import sys

from ....client.state import StateClient
from ....sdk.contracts.dtos.sdk.command_options import CommandOptions
from ....sdk.contracts.errors.server.service import ServiceError

logger = logging.getLogger()


class ContextManager:
    # Application Level Services
    client: StateClient | None = None

    def __init__(self):
        if ContextManager.client is None:
            options: CommandOptions = CommandOptions(sleep_time=5, retry_count=30, tld="localhost:8000", timeout=60)
            ContextManager.client = StateClient(options=options)
            logger.debug("[ContextManager] assigned new state client to context manager")
        else:
            logger.debug("[ContextManager] state client already assigned")


try:
    ContextManager()
except ServiceError as error:
    logger.error(error)
    sys.exit(1)
