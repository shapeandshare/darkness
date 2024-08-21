import logging
import sys
from pathlib import Path

from ....sdk.contracts.dtos.entities.entity import Entity
from ....sdk.contracts.dtos.tiles.chunk import Chunk
from ....sdk.contracts.dtos.tiles.tile import Tile
from ....sdk.contracts.dtos.tiles.world import World
from ....sdk.contracts.errors.server.service import ServiceError
from ...dao.tile import TileDao
from ...services.dao import DaoService

logger = logging.getLogger()

STORAGE_BASE_PATH: Path = Path("..") / "data"


class ContextManager:
    # Application Level Services
    daoservice: DaoService | None = None

    def __init__(self):
        if ContextManager.daoservice is None:
            ContextManager.daoservice = DaoService(
                worlddao=TileDao[World](storage_base_path=STORAGE_BASE_PATH),
                chunkdao=TileDao[Chunk](storage_base_path=STORAGE_BASE_PATH),
                tiledao=TileDao[Tile](storage_base_path=STORAGE_BASE_PATH),
                entitydao=TileDao[Entity](storage_base_path=STORAGE_BASE_PATH),
            )
            logger.debug("[ContextManager] assigned new state service to context manager")
        else:
            logger.debug("[ContextManager] state service already assigned")


try:
    ContextManager()
except ServiceError as error:
    logger.error(error)
    sys.exit(1)
