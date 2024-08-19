import asyncio
import logging
from asyncio import Queue

from ....sdk.contracts.dtos.tiles.address import Address
from ....sdk.contracts.dtos.tiles.chunk import Chunk
from .abstract import AbstractEntityFactory

logger = logging.getLogger()


class EntityFactory(AbstractEntityFactory):
    """ """

    async def terrain_generate(self, tokens: Address, chunk: Chunk) -> None:
        async def step_one():
            async def consumer(queue: Queue):
                while not queue.empty():
                    local_tile_id: str = await queue.get()
                    tokens_tile: Address = Address.model_validate({**tokens.model_dump(), "tile_id": local_tile_id})
                    await self.generate(tokens=tokens_tile)
                    queue.task_done()

            queue = asyncio.Queue()
            await asyncio.gather(EntityFactory.producer(ids=chunk.ids, queue=queue), consumer(queue))

        await step_one()

    async def quantum(self, tokens: Address, chunk: Chunk):
        # Entity Factory Quantum
        async def step_six():
            async def consumer(queue: Queue):
                while not queue.empty():
                    local_tile_id: str = await queue.get()
                    tokens_tile: Address = Address.model_validate({**tokens.model_dump(), "tile_id": local_tile_id})
                    await self.grow_entities(tokens=tokens_tile)
                    queue.task_done()

            queue = asyncio.Queue()
            await asyncio.gather(self.producer(ids=chunk.ids, queue=queue), consumer(queue))

        await step_six()
