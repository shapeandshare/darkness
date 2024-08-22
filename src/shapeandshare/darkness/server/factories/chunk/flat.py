import asyncio
import logging
import uuid
from asyncio import Queue

from ....sdk.contracts.dtos.coordinate import Coordinate
from ....sdk.contracts.dtos.sdk.wrapped_data import WrappedData
from ....sdk.contracts.dtos.tiles.address import Address
from ....sdk.contracts.dtos.tiles.chunk import Chunk
from ....sdk.contracts.dtos.tiles.world import World
from ....sdk.contracts.dtos.window import Window
from ....sdk.contracts.types.tile import TileType
from .abstract import AbstractChunkFactory

logger = logging.getLogger()


class FlatChunkFactory(AbstractChunkFactory):
    async def terrain_generate(self, address: Address, chunk: Chunk) -> None:
        # Lets shovel in some biome default or dirt tiles!
        async def step_one():
            async def consumer(queue: Queue):
                while not queue.empty():
                    local_tile_id: str = await queue.get()
                    address_tile: Address = Address.model_validate({**address.model_dump(), "tile_id": local_tile_id})
                    # Mutate tiles to biome default (or dirt)
                    await self.mutate_tile(
                        address=address_tile,
                        mutate=90,  # percentage of 100%
                        tile_type=(chunk.biome if chunk.biome else TileType.DIRT),
                    )
                    queue.task_done()

            queue = asyncio.Queue()
            await asyncio.gather(FlatChunkFactory.producer(ids=chunk.ids, queue=queue), consumer(queue))

        await step_one()

        # Add Eradicates (rocks)
        async def step_two():
            async def consumer(queue: Queue):
                while not queue.empty():
                    local_tile_id: str = await queue.get()
                    address_tile: Address = Address.model_validate({**address.model_dump(), "tile_id": local_tile_id})
                    await self.mutate_tile(
                        address=address_tile,
                        mutate=0.5,  # 0.5% change (very low)
                        tile_type=TileType.ROCK,
                    )
                    queue.task_done()

            queue = asyncio.Queue()
            await asyncio.gather(self.producer(ids=chunk.ids, queue=queue), consumer(queue))

        await step_two()

        # Convert inner Ocean to Water Tiles
        async def step_three():
            async def consumer(queue: Queue):
                while not queue.empty():
                    local_tile_id: str = await queue.get()
                    address_tile: Address = Address.model_validate({**address.model_dump(), "tile_id": local_tile_id})
                    # Convert inner Ocean to Water Tiles
                    await self.brackish_tile(address=address_tile)
                    queue.task_done()

            queue = asyncio.Queue()
            await asyncio.gather(self.producer(ids=chunk.ids, queue=queue), consumer(queue))

        await step_three()

        # Erode Tiles (to make shore)
        async def step_four():
            async def consumer(queue: Queue):
                while not queue.empty():
                    local_tile_id: str = await queue.get()
                    address_tile: Address = Address.model_validate({**address.model_dump(), "tile_id": local_tile_id})
                    await self.erode_tile(address=address_tile)
                    queue.task_done()

            queue = asyncio.Queue()
            await asyncio.gather(self.producer(ids=chunk.ids, queue=queue), consumer(queue))

        await step_four()

    async def create(self, world_id: str, name: str | None, dimensions: tuple[int, int], biome: TileType) -> Chunk:
        if name is None:
            name = "roshar"

        address_world: Address = Address.model_validate({"world_id": world_id})

        # 1. blank, named chunk
        chunk: Chunk = Chunk(id=str(uuid.uuid4()), name=name, dimensions=dimensions, biome=biome)
        address_chunk: Address = Address.model_validate({**address_world.model_dump(), "chunk_id": chunk.id})
        await self.daoclient.document_post(address=address_chunk, document=chunk)

        # update world metadata
        wrapped_world: WrappedData[World] = await self.daoclient.document_get(address=address_world, full=False)
        wrapped_world.data.ids.add(chunk.id)
        await self.daoclient.document_patch(address=address_world, document={"ids": list(wrapped_world.data.ids)})

        # Define the maximum size
        max_x, max_y = dimensions

        # address["chunk_id"] = chunk.id
        # Generate an empty 2D block of ocean
        window: Window = Window(min=Coordinate(x=1, y=1), max=Coordinate(x=max_x, y=max_y))
        await self.generate_ocean_block(address=address_chunk, window=window)

        chunk: Chunk = (await self.daoclient.document_get(address=address_chunk, full=False)).data

        # Apply our terrain generation
        await self.terrain_generate(address=address_chunk, chunk=chunk)

        # Apply a quantum time
        await self.quantum(world_id=world_id, chunk=chunk)

        # get final state and return
        chunk: Chunk = (await self.daoclient.document_get(address=address_chunk, full=False)).data
        return chunk

    async def quantum(self, world_id: str, chunk: Chunk) -> None:
        address_chunk: Address = Address.model_validate({"world_id": world_id, "chunk_id": chunk.id})

        # Grow Tiles
        async def step_five():
            async def consumer(queue: Queue):
                while not queue.empty():
                    local_tile_id: str = await queue.get()
                    address_tile: Address = Address.model_validate(
                        {**address_chunk.model_dump(), "tile_id": local_tile_id}
                    )
                    await self.grow_tile(address=address_tile)
                    queue.task_done()

            queue = asyncio.Queue()
            await asyncio.gather(self.producer(ids=chunk.ids, queue=queue), consumer(queue))

        await step_five()
