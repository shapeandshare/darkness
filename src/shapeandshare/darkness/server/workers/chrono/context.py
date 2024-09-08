import logging
import sys

from ....client.state import StateClient
from ....sdk.contracts.errors.server.service import ServiceError

logger = logging.getLogger()


class ContextManager:
    # Application Level Services
    client: StateClient | None = None

    @staticmethod
    def deferred_init():
        if ContextManager.client is None:
            ContextManager.client = StateClient()
            logger.debug("[ContextManager] assigned new state client to context manager")
        else:
            logger.debug("[ContextManager] state client already assigned")


# pylint: disable=duplicate-code
try:
    ContextManager()
except ServiceError as error:
    logger.error(error)
    sys.exit(1)
