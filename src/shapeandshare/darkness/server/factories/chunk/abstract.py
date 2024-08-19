import asyncio
import logging
import re
import secrets
import uuid
from abc import abstractmethod
from asyncio import Queue

from pydantic import BaseModel

from ....sdk.contracts.dtos.sdk.wrapped_data import WrappedData
from ....sdk.contracts.dtos.tiles.chunk import Chunk
from ....sdk.contracts.dtos.tiles.tile import Tile
from ....sdk.contracts.dtos.tiles.world import World
from ....sdk.contracts.dtos.window import Window
from ....sdk.contracts.types.connection import TileConnectionType
from ....sdk.contracts.types.tile import TileType
from ...dao.dao import AbstractDao

logger = logging.getLogger()


class AbstractChunkFactory(BaseModel):
    tiledao: AbstractDao[Tile]
    chunkdao: AbstractDao[Chunk]
    worlddao: AbstractDao[World]

    @staticmethod
    async def producer(ids: set[str], queue: Queue):
        for local_id in ids:
            await queue.put(local_id)

    @abstractmethod
    async def create(self, world_id: str, name: str | None, dimensions: tuple[int, int], biome: TileType) -> str:
        """ """

    async def mutate_tile(self, tokens: dict, mutate: float, tile_type: TileType) -> None:
        if secrets.randbelow(100) <= mutate:
            # then we spawn the tile type
            await self.tiledao.patch(tokens=tokens, document={"tile_type": tile_type})

    async def convert_tile(self, tokens: dict, source: TileType, target: TileType) -> None:
        # get
        target_tile: WrappedData[Tile] = await self.tiledao.get(tokens=tokens)
        target_tile.data = Tile.model_validate(target_tile.data)
        # check
        if target_tile.data.tile_type == source:
            # update
            await self.tiledao.patch(tokens=tokens, document={"tile_type": target})

    async def adjecent_liquids(self, tokens: dict) -> list[TileType]:
        return await self.adjecent_to(tokens=tokens, types=[TileType.OCEAN, TileType.WATER])

    async def adjecent_to(self, tokens: dict, types: list[TileType] | None) -> list[TileType]:
        adjecent_targets: list[TileType] = []

        target_tile: WrappedData[Tile] = await self.tiledao.get(tokens=tokens)
        target_tile.data = Tile.model_validate(target_tile.data)

        async def adjecent_producer(queue: Queue):
            for _, adjecent_id in target_tile.data.next.items():
                await queue.put(item={**tokens, "tile_id": adjecent_id})

        async def step_one():
            async def consumer(queue: Queue):
                while not queue.empty():
                    work_item = await queue.get()
                    adjecent_tile: WrappedData[Tile] = await self.tiledao.get(tokens=work_item)
                    adjecent_tile.data = Tile.model_validate(adjecent_tile.data)
                    if adjecent_tile.data.tile_type in types and adjecent_tile.data.tile_type not in adjecent_targets:
                        adjecent_targets.append(adjecent_tile.data.tile_type)
                    queue.task_done()

            queue = asyncio.Queue()
            await asyncio.gather(adjecent_producer(queue), consumer(queue))

        await step_one()

        return adjecent_targets

    async def grow_tile(self, tokens: dict) -> None:
        # get
        target_tile: WrappedData[Tile] = await self.tiledao.get(tokens=tokens)
        target_tile.data = Tile.model_validate(target_tile.data)
        # dirt -> grass
        if target_tile.data.tile_type == TileType.DIRT:
            adjecent_liquids: list[TileType] = await self.adjecent_liquids(tokens=tokens)
            if TileType.WATER in adjecent_liquids and TileType.OCEAN not in adjecent_liquids:
                await self.tiledao.patch(tokens=tokens, document={"tile_type": TileType.GRASS})

        # grass+water (no dirt/ocean) -> forest
        if target_tile.data.tile_type == TileType.GRASS:
            neighbors: list[TileType] = await self.adjecent_to(
                tokens=tokens,
                types=[TileType.WATER, TileType.GRASS, TileType.OCEAN],
            )

            # no forests grow by oceans
            if TileType.OCEAN in neighbors:
                return

            if len(neighbors) > 1:
                # next to more than one kind (grass/water)
                await self.tiledao.patch(tokens=tokens, document={"tile_type": TileType.FOREST})

        # TODO: grass+(dirt)

    async def brackish_tile(self, tokens: dict) -> None:
        # Convert inner Ocean to Water Tiles

        # See if we are next to another ocean tile
        neighbors: list[TileType] = await self.adjecent_to(tokens=tokens, types=[TileType.OCEAN])
        if len(neighbors) < 1:
            await self.convert_tile(tokens=tokens, source=TileType.OCEAN, target=TileType.WATER)

        # TODO: are we an isolated ocean body? if so then we are water
        #
        # # 1. For each next that is liquid (recusively), can we get to the edge?
        # #     # 1. Are we ocean? - if no then return False
        # #     # 2. Are we edge? - if yes then return True
        # #     # 3. then check my nexts
        # #     # 4. Return False (not ocean)

    async def erode_tile(self, tokens: dict) -> None:
        # get
        target_tile: WrappedData[Tile] = await self.tiledao.get(tokens=tokens)
        target_tile.data = Tile.model_validate(target_tile.data)

        # shore erosion
        if target_tile.data.tile_type not in [TileType.UNKNOWN, TileType.OCEAN, TileType.WATER, TileType.SHORE]:
            adjecent_liquids: list[TileType] = await self.adjecent_liquids(tokens=tokens)
            # Apply erosion - rocks and be left by oceans, everything else becomes shore
            if TileType.OCEAN in adjecent_liquids:
                if target_tile.data.tile_type not in (TileType.ROCK, TileType.SHORE):
                    await self.tiledao.patch(tokens=tokens, document={"tile_type": TileType.SHORE})

    async def gen_geo_bind(self, tokens: dict, conn_dir: TileConnectionType, target_tile_id: str) -> None:
        tile_partial: dict = {"next": {conn_dir: target_tile_id}}
        await self.tiledao.patch(tokens=tokens, document=tile_partial)

    async def generate_ocean_block(self, tokens: dict, window: Window):
        tile_map: dict[str, str] = {}

        async def flat_producer(window: Window, queue: Queue):
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

        # 1. fill a blank nXm area with ocean
        async def step_one():
            async def consumer(queue: Queue):
                while not queue.empty():
                    local_tile_id: str = await queue.get()
                    tile_map[local_tile_id] = str(uuid.uuid4())
                    local_tile: Tile = Tile(id=tile_map[local_tile_id], tile_type=TileType.OCEAN)
                    tokens_tile: dict = {**tokens, "tile_id": local_tile.id}

                    # create tile
                    await self.tiledao.post(tokens=tokens_tile, document=local_tile)
                    # msg: str = f"({local_tile_id}) brought into existence as {TileType.OCEAN}"
                    # logger.debug(msg)

                    # Update the chunk --

                    # get
                    wrapped_chunk: WrappedData[Chunk] = await self.chunkdao.get(tokens=tokens)
                    wrapped_chunk.data = Chunk.model_validate(wrapped_chunk.data)

                    wrapped_chunk.data.ids.add(tile_map[local_tile_id])

                    # put -- store chunk update (tile addition)
                    await self.chunkdao.patch(tokens=tokens, document={"ids": wrapped_chunk.data.ids})

                    queue.task_done()

            queue = asyncio.Queue()
            await asyncio.gather(flat_producer(window, queue), consumer(queue))

        await step_one()

        # set origin tile on chunk
        await self.chunkdao.patch(tokens=tokens, document={"origin": tile_map["tile_1_1"]})

        # 2. Connect everything together
        async def step_two():
            pattern: re.Pattern = re.compile("^tile_([a-zA-Z0-9-]+)_([a-zA-Z0-9-]+)$")

            async def consumer(queue):
                while not queue.empty():
                    _local_tile_id: str = await queue.get()
                    local_tile_id = tile_map[_local_tile_id]

                    match = pattern.search(_local_tile_id)
                    # tile_id: str = f"tile_{local_x}_{local_y}"
                    local_x: int = int(match.group(1))
                    local_y: int = int(match.group(2))

                    # msg: str = f"binding ({local_tile_id}) physically to peers"
                    # logger.debug(msg)

                    # Bind LEFT
                    _target_tile_id: str = f"tile_{local_x - 1}_{local_y}"
                    if _target_tile_id in tile_map:
                        target_tile_id = tile_map[_target_tile_id]
                        await self.gen_geo_bind(
                            tokens={**tokens, "tile_id": local_tile_id},
                            target_tile_id=target_tile_id,
                            conn_dir=TileConnectionType.LEFT,
                        )

                    # Bind RIGHT
                    _target_tile_id: str = f"tile_{local_x + 1}_{local_y}"
                    if _target_tile_id in tile_map:
                        target_tile_id = tile_map[_target_tile_id]
                        await self.gen_geo_bind(
                            tokens={**tokens, "tile_id": local_tile_id},
                            target_tile_id=target_tile_id,
                            conn_dir=TileConnectionType.RIGHT,
                        )

                    # Bind UP
                    _target_tile_id: str = f"tile_{local_x}_{local_y - 1}"
                    if _target_tile_id in tile_map:
                        target_tile_id = tile_map[_target_tile_id]
                        await self.gen_geo_bind(
                            tokens={**tokens, "tile_id": local_tile_id},
                            target_tile_id=target_tile_id,
                            conn_dir=TileConnectionType.UP,
                        )

                    # Bind DOWN
                    _target_tile_id: str = f"tile_{local_x}_{local_y + 1}"
                    if _target_tile_id in tile_map:
                        target_tile_id = tile_map[_target_tile_id]
                        await self.gen_geo_bind(
                            tokens={**tokens, "tile_id": local_tile_id},
                            target_tile_id=target_tile_id,
                            conn_dir=TileConnectionType.DOWN,
                        )

                    queue.task_done()

            queue = asyncio.Queue()
            await asyncio.gather(flat_producer(window, queue), consumer(queue))

        await step_two()
