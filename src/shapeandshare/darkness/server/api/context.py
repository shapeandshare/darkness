import logging
import sys

from ...sdk.contracts.errors.server.service import ServiceError
from ..services.world import WorldService

logger = logging.getLogger()


class ContextManager:
    # Application Level Services
    world_service: WorldService | None = None

    def __init__(self):
        if ContextManager.world_service is None:
            ContextManager.world_service = WorldService()
            logger.debug("[ContextManager] assigned new world service to context manager")
        else:
            logger.debug("[ContextManager] world service already assigned")


try:
    ContextManager()
except ServiceError as error:
    logger.error(error)
    sys.exit(1)
