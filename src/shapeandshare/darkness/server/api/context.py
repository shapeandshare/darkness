import logging
import sys
from pathlib import Path

from ...sdk.contracts.errors.server.service import ServiceError
from ..dao.entity import EntityDao
from ..dao.island import IslandDao
from ..dao.tile import TileDao
from ..dao.world import WorldDao
from ..factories.entity.entity import EntityFactory
from ..factories.island.flat import FlatIslandFactory
from ..factories.world.world import WorldFactory
from ..services.state import StateService

logger = logging.getLogger()

STORAGE_BASE_PATH: Path = Path(".") / "data"


class ContextManager:
    # Application Level Services
    state_service: StateService | None = None

    def __init__(self):
        if ContextManager.state_service is None:
            worlddao = WorldDao(storage_base_path=STORAGE_BASE_PATH)
            islanddao = IslandDao(storage_base_path=STORAGE_BASE_PATH)
            tiledao = TileDao(storage_base_path=STORAGE_BASE_PATH)
            entitydao = EntityDao(storage_base_path=STORAGE_BASE_PATH)

            world_factory = WorldFactory(worlddao=worlddao)
            entity_factory = EntityFactory(entitydao=entitydao)
            flatisland_factory = FlatIslandFactory(islanddao=islanddao, tiledao=tiledao, entity_factory=entity_factory)

            ContextManager.state_service = StateService(worlddao=worlddao, islanddao=islanddao, tiledao=tiledao, world_factory=world_factory, flatisland_factory=flatisland_factory)
            logger.debug("[ContextManager] assigned new state service to context manager")
        else:
            logger.debug("[ContextManager] state service already assigned")


try:
    ContextManager()
except ServiceError as error:
    logger.error(error)
    sys.exit(1)
