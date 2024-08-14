import asyncio
import logging
import uuid
from asyncio import Queue

from ....sdk.contracts.dtos.coordinate import Coordinate
from ....sdk.contracts.dtos.tiles.island import Island
from ....sdk.contracts.dtos.window import Window
from ....sdk.contracts.types.tile import TileType
from ...dao.entity import EntityDao
from ...dao.tile import TileDao
from .abstract import AbstractEntityFactory

# from .abstract import AbstractEntityFactory

logger = logging.getLogger()


class EntityFactory(AbstractEntityFactory):
    """ """

    async def quantum(self, world_id: str, island_id: str, window: Window):
        # Entity Factory Quantum
        async def step_six():
            async def consumer(queue: Queue):
                while not queue.empty():
                    local_tile_id: str = await queue.get()
                    await self.grow_entities(world_id=world_id, island_id=island_id, tile_id=local_tile_id)
                    queue.task_done()

            queue = asyncio.Queue()
            await asyncio.gather(self.producer(window, queue), consumer(queue))

        await step_six()
