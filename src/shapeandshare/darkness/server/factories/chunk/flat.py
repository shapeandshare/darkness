import asyncio
import logging
import uuid
from asyncio import Queue

from ....sdk.contracts.dtos.coordinate import Coordinate
from ....sdk.contracts.dtos.sdk.wrapped_data import WrappedData
from ....sdk.contracts.dtos.tiles.chunk import Chunk
from ....sdk.contracts.dtos.tiles.world import World
from ....sdk.contracts.dtos.window import Window
from ....sdk.contracts.types.tile import TileType
from .abstract import AbstractChunkFactory

logger = logging.getLogger()


class FlatChunkFactory(AbstractChunkFactory):
    async def terrain_generate(self, world_id: str, chunk: Chunk) -> None:
        tokens: dict = {"world_id": world_id, "chunk_id": chunk.id}

        # Lets shovel in some biome default or dirt tiles!
        async def step_one():
            async def consumer(queue: Queue):
                while not queue.empty():
                    local_tile_id: str = await queue.get()
                    # Mutate tiles to biome default (or dirt)
                    await self.mutate_tile(
                        tokens={**tokens, "tile_id": local_tile_id},
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
                    await self.mutate_tile(
                        tokens={**tokens, "tile_id": local_tile_id},
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
                    # Convert inner Ocean to Water Tiles
                    await self.brackish_tile(tokens={**tokens, "tile_id": local_tile_id})
                    queue.task_done()

            queue = asyncio.Queue()
            await asyncio.gather(self.producer(ids=chunk.ids, queue=queue), consumer(queue))

        await step_three()

        # Erode Tiles (to make shore)
        async def step_four():
            async def consumer(queue: Queue):
                while not queue.empty():
                    local_tile_id: str = await queue.get()
                    await self.erode_tile(tokens={**tokens, "tile_id": local_tile_id})
                    queue.task_done()

            queue = asyncio.Queue()
            await asyncio.gather(self.producer(ids=chunk.ids, queue=queue), consumer(queue))

        await step_four()

    async def create(self, world_id: str, name: str | None, dimensions: tuple[int, int], biome: TileType) -> Chunk:
        if name is None:
            name = "roshar"

        tokens: dict = {"world_id": world_id}

        # 1. blank, named chunk
        chunk: Chunk = Chunk(id=str(uuid.uuid4()), name=name, dimensions=dimensions, biome=biome)
        await self.chunkdao.post(tokens=tokens, document=chunk)

        # update world metadata
        wrapped_world: WrappedData[World] = await self.worlddao.get(tokens=tokens)
        wrapped_world.data = World.model_validate(wrapped_world.data)
        wrapped_world.data.ids.add(chunk.id)
        await self.worlddao.patch(tokens=tokens, document={"ids": wrapped_world.data.ids})

        # Define the maximum size
        max_x, max_y = dimensions

        tokens["chunk_id"] = chunk.id
        # Generate an empty 2D block of ocean
        window: Window = Window(min=Coordinate(x=1, y=1), max=Coordinate(x=max_x, y=max_y))
        await self.generate_ocean_block(tokens=tokens, window=window)
        chunk = Chunk.model_validate((await self.chunkdao.get(tokens=tokens)).data)

        # Apply our terrain generation
        await self.terrain_generate(world_id=world_id, chunk=chunk)

        # Apply a quantum time
        await self.quantum(world_id=world_id, chunk=chunk)

        # get final state and return
        return Chunk.model_validate((await self.chunkdao.get(tokens=tokens)).data)

    async def quantum(self, world_id: str, chunk: Chunk) -> None:
        tokens: dict = {"world_id": world_id, "chunk_id": chunk.id}

        # Grow Tiles
        async def step_five():
            async def consumer(queue: Queue):
                while not queue.empty():
                    local_tile_id: str = await queue.get()
                    await self.grow_tile(tokens={**tokens, "tile_id": local_tile_id})
                    queue.task_done()

            queue = asyncio.Queue()
            await asyncio.gather(self.producer(ids=chunk.ids, queue=queue), consumer(queue))

        await step_five()
