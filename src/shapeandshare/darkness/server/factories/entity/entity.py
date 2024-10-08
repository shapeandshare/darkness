import asyncio
import logging
from asyncio import Queue

from ....sdk.contracts.dtos.tiles.address import Address
from ....sdk.contracts.dtos.tiles.chunk import Chunk
from .abstract import AbstractEntityFactory

logger = logging.getLogger()


class EntityFactory(AbstractEntityFactory):
    """ """

    async def terrain_generate(self, address: Address, chunk: Chunk) -> None:
        async def step_one():
            async def consumer(queue: Queue):
                while not queue.empty():
                    local_tile_id: str = await queue.get()
                    address_tile: Address = Address.model_validate({**address.model_dump(), "tile_id": local_tile_id})
                    await self.generate(address=address_tile)
                    queue.task_done()

            queue = asyncio.Queue()
            await asyncio.gather(EntityFactory.producer(ids=chunk.ids, queue=queue), consumer(queue))

        await step_one()

    async def quantum(self, address: Address):
        chunk: Chunk = await self.daoclient.get(address=address)

        # Entity Factory Quantum
        async def step_six():
            async def consumer(queue: Queue):
                while not queue.empty():
                    local_tile_id: str = await queue.get()
                    address_tile: Address = Address.model_validate({**address.model_dump(), "tile_id": local_tile_id})
                    await self.grow_entities(address=address_tile)
                    queue.task_done()

            queue = asyncio.Queue()
            await asyncio.gather(self.producer(ids=chunk.ids, queue=queue), consumer(queue))

        await step_six()
