import logging
import sys

from ....sdk.contracts.errors.server.service import ServiceError
from ...clients.dao import DaoClient, get_mongodb
from ...factories.chunk.flat import FlatChunkFactory
from ...factories.entity.entity import EntityFactory
from ...factories.world.world import WorldFactory
from ...services.state import StateService

logger = logging.getLogger()


class ContextManager:
    # Application Level Services
    state_service: StateService | None = None

    @staticmethod
    def deferred_init():
        if ContextManager.state_service is None:
            daoclient: DaoClient = DaoClient(database=get_mongodb())

            world_factory = WorldFactory(daoclient=daoclient)
            entity_factory = EntityFactory(daoclient=daoclient)
            flatchunk_factory = FlatChunkFactory(daoclient=daoclient, entity_factory=entity_factory)

            ContextManager.state_service = StateService(
                daoclient=daoclient,
                entity_factory=entity_factory,
                world_factory=world_factory,
                flatchunk_factory=flatchunk_factory,
            )
            logger.debug("[ContextManager] assigned new state service to context manager")
        else:
            logger.debug("[ContextManager] state service already assigned")


# pylint: disable=duplicate-code
try:
    ContextManager()
except ServiceError as error:
    logger.error(error)
    sys.exit(1)
