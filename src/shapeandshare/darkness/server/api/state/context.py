import logging
import sys

from ....client.dao import DaoClient, get_mongodb
from ....sdk.contracts.errors.server.service import ServiceError
from ...factories.chunk.flat import FlatChunkFactory
from ...factories.entity.entity import EntityFactory
from ...factories.world.world import WorldFactory
from ...services.state import StateService

logger = logging.getLogger()


class ContextManager:
    # Application Level Services
    state_service: StateService | None = None

    def __init__(self):
        if ContextManager.state_service is None:
            daoclient: DaoClient = DaoClient(
                database=get_mongodb(hostname="127.0.0.1", port=27017, database="darkness")
            )

            world_factory = WorldFactory(daoclient=daoclient)
            entity_factory = EntityFactory(daoclient=daoclient)
            flatchunk_factory = FlatChunkFactory(daoclient=daoclient)

            ContextManager.state_service = StateService(
                daoclient=daoclient,
                entity_factory=entity_factory,
                world_factory=world_factory,
                flatchunk_factory=flatchunk_factory,
            )
            logger.debug("[ContextManager] assigned new state service to context manager")
        else:
            logger.debug("[ContextManager] state service already assigned")


try:
    ContextManager()
except ServiceError as error:
    logger.error(error)
    sys.exit(1)
