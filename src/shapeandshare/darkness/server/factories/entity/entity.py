import asyncio
import logging
from asyncio import Queue

from ....sdk.contracts.dtos.tiles.island import Island
from .abstract import AbstractEntityFactory

logger = logging.getLogger()


class EntityFactory(AbstractEntityFactory):
    """ """

    async def terrain_generate(self, world_id: str, island: Island) -> None:
        async def step_one():
            async def consumer(queue: Queue):
                while not queue.empty():
                    local_tile_id: str = await queue.get()
                    await self.generate(tokens={"world_id": world_id, "island_id": island.id, "tile_id": local_tile_id})
                    queue.task_done()

            queue = asyncio.Queue()
            await asyncio.gather(EntityFactory.producer(ids=island.ids, queue=queue), consumer(queue))

        await step_one()

    async def quantum(self, world_id: str, island: Island):
        # Entity Factory Quantum
        async def step_six():
            async def consumer(queue: Queue):
                while not queue.empty():
                    local_tile_id: str = await queue.get()
                    await self.grow_entities(world_id=world_id, island_id=island.id, tile_id=local_tile_id)
                    queue.task_done()

            queue = asyncio.Queue()
            await asyncio.gather(self.producer(ids=island.ids, queue=queue), consumer(queue))

        await step_six()
