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
from .abstract import AbstractIslandFactory

logger = logging.getLogger()


class FlatIslandFactory(AbstractIslandFactory):
    tiledao: TileDao
    entitydao: EntityDao

    async def terrain_generate(self, world_id: str, island: Island, window: Window) -> None:
        # Lets shovel in some biome default or dirt tiles!
        async def step_one():
            async def consumer(queue: Queue):
                while not queue.empty():
                    local_tile_id: str = await queue.get()
                    # Mutate tiles to biome default (or dirt)
                    await self.mutate_tile(
                        world_id=world_id,
                        island_id=island.id,
                        tile_id=local_tile_id,
                        mutate=90,  # percentage of 100%
                        tile_type=(island.biome if island.biome else TileType.DIRT),
                    )
                    queue.task_done()

            queue = asyncio.Queue()
            await asyncio.gather(FlatIslandFactory.producer(window, queue), consumer(queue))

        await step_one()

        # Add Eradicates (rocks)
        async def step_two():
            async def consumer(queue: Queue):
                while not queue.empty():
                    local_tile_id: str = await queue.get()
                    await self.mutate_tile(
                        world_id=world_id,
                        island_id=island.id,
                        tile_id=local_tile_id,
                        mutate=0.5,  # 0.5% change (very low)
                        tile_type=TileType.ROCK,
                    )
                    queue.task_done()

            queue = asyncio.Queue()
            await asyncio.gather(self.producer(window, queue), consumer(queue))

        await step_two()

    async def create(self, world_id: str, name: str | None, dimensions: tuple[int, int], biome: TileType) -> Island:
        if name is None:
            name = "roshar"

        # 1. blank, named island
        island: Island = Island(id=str(uuid.uuid4()), name=name, dimensions=dimensions, biome=biome)
        await self.islanddao.post(world_id=world_id, island=island)

        # Define the maximum size
        max_x, max_y = dimensions

        # Generate an empty 2D block of ocean
        window: Window = Window(min=Coordinate(x=1, y=1), max=Coordinate(x=max_x, y=max_y))
        await self.generate_ocean_block(world_id=world_id, island_id=island.id, window=window)

        # Apply our terrain generation
        window = Window(min=Coordinate(x=2, y=2), max=Coordinate(x=max_x - 1, y=max_y - 1))
        await self.terrain_generate(world_id=world_id, island=island, window=window)

        # Apply a quantum time
        window = Window(min=Coordinate(x=1, y=1), max=Coordinate(x=max_x, y=max_y))
        await self.quantum(world_id=world_id, island=island, window=window)

        # get final state and return
        return (await self.islanddao.get(world_id=world_id, island_id=island.id)).data

    async def quantum(self, world_id: str, island: Island, window: Window):
        # TODO: isolated ocean is NOT ocean, we MUST have path to the edge
        # Convert inner Ocean to Water Tiles
        async def step_three():
            async def consumer(queue: Queue):
                while not queue.empty():
                    local_tile_id: str = await queue.get()
                    # Convert inner Ocean to Water Tiles
                    await self.brackish_tile(world_id=world_id, island_id=island.id, tile_id=local_tile_id)
                    queue.task_done()

            queue = asyncio.Queue()
            await asyncio.gather(self.producer(window, queue), consumer(queue))

        await step_three()

        # Erode Tiles (to make shore)
        async def step_four():
            async def consumer(queue: Queue):
                while not queue.empty():
                    local_tile_id: str = await queue.get()
                    await self.erode_tile(world_id=world_id, island_id=island.id, tile_id=local_tile_id)
                    queue.task_done()

            queue = asyncio.Queue()
            await asyncio.gather(self.producer(window, queue), consumer(queue))

        await step_four()

        # Grow Tiles
        async def step_five():
            async def consumer(queue: Queue):
                while not queue.empty():
                    local_tile_id: str = await queue.get()
                    await self.grow_tile(world_id=world_id, island_id=island.id, tile_id=local_tile_id)
                    queue.task_done()

            queue = asyncio.Queue()
            await asyncio.gather(self.producer(window, queue), consumer(queue))

        await step_five()
