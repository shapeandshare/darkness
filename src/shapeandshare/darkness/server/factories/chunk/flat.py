import asyncio
import logging
import uuid
from asyncio import Queue

from ....sdk.contracts.dtos.coordinate import Coordinate
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
                        mutate=3750,  # percentage of 100%
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
                        mutate=10,  # 0.5% change (very low)
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
        await self.daoclient.post(address=address_chunk, document=chunk)

        # update world metadata
        world: World = await self.daoclient.get(address=address_world)
        world.ids.add(chunk.id)
        await self.daoclient.patch(address=address_world, document={"ids": list(world.ids)})

        # Define the maximum size
        max_x, max_y = dimensions

        # address["chunk_id"] = chunk.id
        # Generate an empty 2D block of ocean
        window: Window = Window(min=Coordinate(x=1, y=1), max=Coordinate(x=max_x, y=max_y))
        await self.generate_ocean_block(address=address_chunk, window=window)

        chunk: Chunk = await self.daoclient.get(address=address_chunk)

        # Apply our terrain generation
        await self.terrain_generate(address=address_chunk, chunk=chunk)

        # get final state and return
        return await self.daoclient.get(address=address_chunk)

    async def quantum(self, address: Address) -> None:
        chunk: Chunk = await self.daoclient.get(address=address)

        # Grow Tiles
        async def step_five():
            async def consumer(queue: Queue):
                while not queue.empty():
                    local_tile_id: str = await queue.get()
                    address_tile: Address = Address.model_validate({**address.model_dump(), "tile_id": local_tile_id})
                    await self.tile_grow(address=address_tile)
                    await self.tile_senescence(address=address_tile)
                    queue.task_done()

            queue = asyncio.Queue()
            await asyncio.gather(self.producer(ids=chunk.ids, queue=queue), consumer(queue))

        await step_five()
