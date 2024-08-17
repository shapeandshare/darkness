import asyncio
import logging
import uuid
from asyncio import Queue

from .... import World, WrappedData
from ....sdk.contracts.dtos.coordinate import Coordinate
from ....sdk.contracts.dtos.tiles.island import Island
from ....sdk.contracts.dtos.window import Window
from ....sdk.contracts.types.tile import TileType
from .abstract import AbstractIslandFactory

logger = logging.getLogger()


class FlatIslandFactory(AbstractIslandFactory):
    async def terrain_generate(self, world_id: str, island: Island) -> None:
        tokens: dict = {"world_id": world_id, "island_id": island.id}

        # Lets shovel in some biome default or dirt tiles!
        async def step_one():
            async def consumer(queue: Queue):
                while not queue.empty():
                    local_tile_id: str = await queue.get()
                    # Mutate tiles to biome default (or dirt)
                    await self.mutate_tile(
                        tokens={**tokens, "tile_id": local_tile_id},
                        mutate=90,  # percentage of 100%
                        tile_type=(island.biome if island.biome else TileType.DIRT),
                    )
                    queue.task_done()

            queue = asyncio.Queue()
            await asyncio.gather(FlatIslandFactory.producer(ids=island.ids, queue=queue), consumer(queue))

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
            await asyncio.gather(self.producer(ids=island.ids, queue=queue), consumer(queue))

        await step_two()

    async def create(self, world_id: str, name: str | None, dimensions: tuple[int, int], biome: TileType) -> Island:
        if name is None:
            name = "roshar"

        tokens: dict = {"world_id": world_id}

        # 1. blank, named island
        island: Island = Island(id=str(uuid.uuid4()), name=name, dimensions=dimensions, biome=biome)
        await self.islanddao.post(tokens=tokens, document=island)

        # update world metadata
        wrapped_world: WrappedData[World] = await self.worlddao.get(tokens=tokens)
        wrapped_world.data = World.model_validate(wrapped_world.data)
        wrapped_world.data.ids.add(island.id)
        await self.worlddao.patch(tokens=tokens, document={"ids": wrapped_world.data.ids})

        # Define the maximum size
        max_x, max_y = dimensions

        tokens["island_id"] = island.id
        # Generate an empty 2D block of ocean
        window: Window = Window(min=Coordinate(x=1, y=1), max=Coordinate(x=max_x, y=max_y))
        await self.generate_ocean_block(tokens=tokens, window=window)
        island = Island.model_validate((await self.islanddao.get(tokens=tokens)).data)

        # Apply our terrain generation
        await self.terrain_generate(world_id=world_id, island=island)

        # Apply a quantum time
        await self.quantum(world_id=world_id, island=island)

        # get final state and return
        return Island.model_validate((await self.islanddao.get(tokens=tokens)).data)

    async def quantum(self, world_id: str, island: Island) -> None:
        tokens: dict = {"world_id": world_id, "island_id": island.id}

        # Convert inner Ocean to Water Tiles
        async def step_three():
            async def consumer(queue: Queue):
                while not queue.empty():
                    local_tile_id: str = await queue.get()
                    # Convert inner Ocean to Water Tiles
                    await self.brackish_tile(tokens={**tokens, "tile_id": local_tile_id})
                    queue.task_done()

            queue = asyncio.Queue()
            await asyncio.gather(self.producer(ids=island.ids, queue=queue), consumer(queue))

        await step_three()

        # Erode Tiles (to make shore)
        async def step_four():
            async def consumer(queue: Queue):
                while not queue.empty():
                    local_tile_id: str = await queue.get()
                    await self.erode_tile(tokens={**tokens, "tile_id": local_tile_id})
                    queue.task_done()

            queue = asyncio.Queue()
            await asyncio.gather(self.producer(ids=island.ids, queue=queue), consumer(queue))

        await step_four()

        # Grow Tiles
        async def step_five():
            async def consumer(queue: Queue):
                while not queue.empty():
                    local_tile_id: str = await queue.get()
                    await self.grow_tile(tokens={**tokens, "tile_id": local_tile_id})
                    queue.task_done()

            queue = asyncio.Queue()
            await asyncio.gather(self.producer(ids=island.ids, queue=queue), consumer(queue))

        await step_five()
