import logging
import sys
from pathlib import Path

from ....client.dao import DaoClient
from ....sdk.contracts.dtos.entities.entity import Entity
from ....sdk.contracts.dtos.sdk.command_options import CommandOptions
from ....sdk.contracts.dtos.tiles.chunk import Chunk
from ....sdk.contracts.dtos.tiles.tile import Tile
from ....sdk.contracts.dtos.tiles.world import World
from ....sdk.contracts.errors.server.service import ServiceError
from ...dao.tile import TileDao
from ...factories.chunk.flat import FlatChunkFactory
from ...factories.entity.entity import EntityFactory
from ...factories.world.world import WorldFactory
from ...services.dao import DaoService
from ...services.state import StateService

logger = logging.getLogger()

STORAGE_BASE_PATH: Path = Path(".") / "data"


class ContextManager:
    # Application Level Services
    state_service: StateService | None = None

    def __init__(self):
        if ContextManager.state_service is None:
            options: CommandOptions = CommandOptions(sleep_time=5, retry_count=30, tld="127.0.0.1:8001", timeout=60)
            daoclient: DaoClient = DaoClient(options=options)

            worlddao = TileDao[World](storage_base_path=STORAGE_BASE_PATH)
            chunkdao = TileDao[Chunk](storage_base_path=STORAGE_BASE_PATH)
            tiledao = TileDao[Tile](storage_base_path=STORAGE_BASE_PATH)
            entitydao = TileDao[Entity](storage_base_path=STORAGE_BASE_PATH)
            daoservice: DaoService = DaoService(
                worlddao=worlddao, chunkdao=chunkdao, tiledao=tiledao, entitydao=entitydao
            )

            world_factory = WorldFactory(daoclient=daoclient)
            entity_factory = EntityFactory(daoservice=daoservice, daoclient=daoclient)
            flatchunk_factory = FlatChunkFactory(daoclient=daoclient)

            ContextManager.state_service = StateService(
                daoservice=daoservice,
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
