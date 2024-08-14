# import asyncio
import logging
from asyncio import Queue

from pydantic import BaseModel

from ....sdk.contracts.dtos.window import Window
from ...dao.entity import EntityDao

# from src.shapeandshare.darkness.sdk.contracts.dtos.window import Window


# import re
# import secrets
# from abc import abstractmethod
# from asyncio import Queue


# from ....sdk.contracts.dtos.sdk.wrapped_data import WrappedData
# from ....sdk.contracts.dtos.tiles.island import Island
# from ....sdk.contracts.dtos.tiles.tile import Tile
# from ....sdk.contracts.dtos.window import Window
# from ....sdk.contracts.errors.server.dao.inconsistency import DaoInconsistencyError
# from ....sdk.contracts.types.connection import TileConnectionType
# from ....sdk.contracts.types.tile import TileType
# from ...dao.island import IslandDao

logger = logging.getLogger()


class AbstractEntityFactory(BaseModel):
    entitydao: EntityDao

    @staticmethod
    async def producer(window: Window, queue: Queue):
        range_x_min: int = window.min.x - 1
        range_x_max: int = window.max.x
        range_y_min: int = window.min.x - 1
        range_y_max: int = window.max.y

        for x in range(range_x_min, range_x_max):
            for y in range(range_y_min, range_y_max):
                local_x = x + 1
                local_y = y + 1
                tile_id: str = f"tile_{local_x}_{local_y}"
                await queue.put(tile_id)

    async def grow_entities(self, world_id: str, island_id: str, tile_id: str):
        pass

    # @abstractmethod
    # async def create(self, world_id: str, name: str | None, dimensions: tuple[int, int], biome: TileType) -> str:
    #     """ """
