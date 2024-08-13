import logging
import sys
from pathlib import Path

from ...sdk.contracts.errors.server.service import ServiceError
from ..dao.entity import EntityDao
from ..dao.island import IslandDao
from ..dao.tile import TileDao
from ..dao.world import WorldDao
from ..services.state import StateService

logger = logging.getLogger()

STORAGE_BASE_PATH: Path = Path(".") / "data"


class ContextManager:
    # Application Level Services
    state_service: StateService | None = None

    def __init__(self):
        if ContextManager.state_service is None:
            ContextManager.state_service = StateService(
                worlddao=WorldDao(storage_base_path=STORAGE_BASE_PATH),
                islanddao=IslandDao(storage_base_path=STORAGE_BASE_PATH),
                tiledao=TileDao(storage_base_path=STORAGE_BASE_PATH),
                entitydao=EntityDao(storage_base_path=STORAGE_BASE_PATH),
            )
            logger.debug("[ContextManager] assigned new state service to context manager")
        else:
            logger.debug("[ContextManager] state service already assigned")


try:
    ContextManager()
except ServiceError as error:
    logger.error(error)
    sys.exit(1)
