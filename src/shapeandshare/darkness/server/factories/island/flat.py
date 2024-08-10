import logging
import secrets
import uuid

from ....sdk.contracts.dtos.coordinate import Coordinate
from ....sdk.contracts.dtos.island_lite import IslandLite
from ....sdk.contracts.dtos.sdk.wrapped_data import WrappedData
from ....sdk.contracts.dtos.tile import Tile
from ....sdk.contracts.dtos.window import Window
from ....sdk.contracts.types.connection import TileConnectionType
from ....sdk.contracts.types.tile import TileType
from ...dao.tile import TileDao
from .abstract import AbstractIslandFactory

logger = logging.getLogger()


class FlatIslandFactory(AbstractIslandFactory):
    tiledao: TileDao

    async def tiles_process(self, world_id: str, island: IslandLite, window: Window) -> None:
        range_x_min: int = window.min.x - 1
        range_x_max: int = window.max.x
        range_y_min: int = window.min.x - 1
        range_y_max: int = window.max.y

        # Lets shovel in some biome default or dirt tiles!
        for x in range(range_x_min, range_x_max):
            for y in range(range_y_min, range_y_max):
                local_x = x + 1
                local_y = y + 1
                tile_id: str = f"tile_{local_x}_{local_y}"

                # Mutate tiles to biome default (or dirt)
                await self.mutate_tile(
                    world_id=world_id,
                    island_id=island.id,
                    tile_id=tile_id,
                    mutate=90,  # percentage of 100%
                    tile_type=(island.biome if island.biome else TileType.DIRT),
                )

        # Add Eradicates (rocks)
        for x in range(range_x_min, range_x_max):
            for y in range(range_y_min, range_y_max):
                local_x = x + 1
                local_y = y + 1
                tile_id: str = f"tile_{local_x}_{local_y}"
                await self.mutate_tile(
                    world_id=world_id,
                    island_id=island.id,
                    tile_id=tile_id,
                    mutate=0.5,  # 0.5% change (very low)
                    tile_type=TileType.ROCK,
                )

        # TODO: isolated ocean is NOT ocean, we MUST have path to the edge
        # Convert inner Ocean to Water Tiles
        for x in range(range_x_min, range_x_max):
            for y in range(range_y_min, range_y_max):
                local_x = x + 1
                local_y = y + 1
                tile_id: str = f"tile_{local_x}_{local_y}"

                # Convert inner Ocean to Water Tiles
                await self.brackish_tile(world_id=world_id, island_id=island.id, tile_id=tile_id)

        # Erode Tiles (to make shore)
        for x in range(range_x_min, range_x_max):
            for y in range(range_y_min, range_y_max):
                local_x = x + 1
                local_y = y + 1
                tile_id: str = f"tile_{local_x}_{local_y}"

                # Erode Tiles
                await self.erode_tile(world_id=world_id, island_id=island.id, tile_id=tile_id)

        # Grow Tiles
        for x in range(range_x_min, range_x_max):
            for y in range(range_y_min, range_y_max):
                local_x = x + 1
                local_y = y + 1
                tile_id: str = f"tile_{local_x}_{local_y}"

                # Grow Tiles
                await self.grow_tile(world_id=world_id, island_id=island.id, tile_id=tile_id)

    async def mutate_tile(
        self, world_id: str, island_id: str, tile_id: str, mutate: float, tile_type: TileType
    ) -> None:
        if secrets.randbelow(100) <= mutate:
            # then we spawn the tile type
            # island.tiles[tile_id].tile_type = type

            # We don't current have a patch, so get and put..
            # get
            target_tile: WrappedData[Tile] = await self.tiledao.get(
                world_id=world_id, island_id=island_id, tile_id=tile_id
            )
            # patch
            target_tile.data.tile_type = tile_type
            # put
            await self.tiledao.put_safe(world_id=world_id, island_id=island_id, wrapped_tile=target_tile)

    async def convert_tile(
        self, world_id: str, island_id: str, tile_id: str, source: TileType, target: TileType
    ) -> None:
        # get
        target_tile: WrappedData[Tile] = await self.tiledao.get(world_id=world_id, island_id=island_id, tile_id=tile_id)

        # check
        if target_tile.data.tile_type == source:
            # patch
            target_tile.data.tile_type = target

            # put
            await self.tiledao.put_safe(world_id=world_id, island_id=island_id, wrapped_tile=target_tile)

    async def adjecent_liquids(self, world_id: str, island_id: str, tile_id: str) -> list[TileType]:
        return await self.adjecent_to(
            world_id=world_id, island_id=island_id, tile_id=tile_id, types=[TileType.OCEAN, TileType.WATER]
        )

    async def adjecent_to(
        self, world_id: str, island_id: str, tile_id: str, types: list[TileType] | None
    ) -> list[TileType]:
        adjecent_targets: list[TileType] = []

        target_tile: WrappedData[Tile] = await self.tiledao.get(world_id=world_id, island_id=island_id, tile_id=tile_id)
        for _, adjecent_id in target_tile.data.next.items():

            adjecent_tile: WrappedData[Tile] = await self.tiledao.get(
                world_id=world_id, island_id=island_id, tile_id=adjecent_id
            )
            # logger.debug(f"tile {tile_id} -> {adjecent_dir} -> {adjecent_id} -> {adjecent_tile.data.tile_type}")

            if adjecent_tile.data.tile_type in types and adjecent_tile.data.tile_type not in adjecent_targets:
                adjecent_targets.append(adjecent_tile.data.tile_type)
        # logger.debug(f"tile {tile_id} is adjecent to: {adjecent_targets}")
        return adjecent_targets

    async def grow_tile(self, world_id: str, island_id: str, tile_id: str) -> None:
        # if island.tiles[tile_id].tile_type not in [TileType.UNKNOWN, TileType.OCEAN, TileType.WATER]:

        # get
        target_tile: WrappedData[Tile] = await self.tiledao.get(world_id=world_id, island_id=island_id, tile_id=tile_id)

        # dirt -> grass
        if target_tile.data.tile_type == TileType.DIRT:
            adjecent_liquids: list[TileType] = await self.adjecent_liquids(
                world_id=world_id, island_id=island_id, tile_id=tile_id
            )
            if TileType.WATER in adjecent_liquids and TileType.OCEAN not in adjecent_liquids:
                # patch
                target_tile.data.tile_type = TileType.GRASS

                # put
                await self.tiledao.put_safe(world_id=world_id, island_id=island_id, wrapped_tile=target_tile)

        # grass+water (no dirt/ocean) -> forest
        if target_tile.data.tile_type == TileType.GRASS:
            neighbors: list[TileType] = await self.adjecent_to(
                world_id=world_id,
                island_id=island_id,
                tile_id=tile_id,
                types=[TileType.WATER, TileType.GRASS, TileType.OCEAN],
            )

            # no forests grow by oceans
            if TileType.OCEAN in neighbors:
                return

            if len(neighbors) > 1:
                # next to more than one kind (grass/water)

                # patch
                target_tile.data.tile_type = TileType.FOREST

                # put
                await self.tiledao.put_safe(world_id=world_id, island_id=island_id, wrapped_tile=target_tile)

        # # grass+(dirt)
        # if island.tiles[tile_id].tile_type == TileType.GRASS:
        #     neighbors: list[TileType] = FlatIslandFactory.adjecent_to(
        #         # TODO: review this josh ...
        #         island=island, tile_id=tile_id, types=[TileType.WATER, TileType.GRASS, TileType.DIRT, TileType.FOREST]
        #     )

    async def brackish_tile(self, world_id: str, island_id: str, tile_id: str):
        # Convert inner Ocean to Water Tiles

        # See if we are next to ocean
        neighbors: list[TileType] = await self.adjecent_to(
            world_id=world_id, island_id=island_id, tile_id=tile_id, types=[TileType.OCEAN]
        )
        if len(neighbors) < 1:
            await self.convert_tile(
                world_id=world_id, island_id=island_id, tile_id=tile_id, source=TileType.OCEAN, target=TileType.WATER
            )

    async def erode_tile(self, world_id: str, island_id: str, tile_id: str) -> None:
        msg: str = f"eroding tile: {tile_id}"
        logger.debug(msg)

        # get
        target_tile: WrappedData[Tile] = await self.tiledao.get(world_id=world_id, island_id=island_id, tile_id=tile_id)

        # shore erosion
        if target_tile.data.tile_type not in [TileType.UNKNOWN, TileType.OCEAN, TileType.WATER, TileType.SHORE]:
            adjecent_liquids: list[TileType] = await self.adjecent_liquids(
                world_id=world_id, island_id=island_id, tile_id=tile_id
            )
            # Apply erosion - rocks and be left by oceans, everything else becomes shore
            if TileType.OCEAN in adjecent_liquids:
                if target_tile.data.tile_type not in (TileType.ROCK, TileType.SHORE):
                    previous_type = target_tile.data.tile_type

                    # patch
                    target_tile.data.tile_type = TileType.SHORE

                    # put
                    await self.tiledao.put_safe(world_id=world_id, island_id=island_id, wrapped_tile=target_tile)

                    msg: str = f"tile {tile_id}:{previous_type} converted to {TileType.SHORE}"
                    logger.debug(msg)

    async def generate_ocean_block(self, world_id: str, island_id: str, window: Window):
        # 1. fill a blank nXm area with ocean
        range_x_min: int = window.min.x - 1
        range_x_max: int = window.max.x
        range_y_min: int = window.min.x - 1
        range_y_max: int = window.max.y
        for x in range(range_x_min, range_x_max):
            for y in range(range_y_min, range_y_max):
                local_x = x + 1
                local_y = y + 1

                tile_id: str = f"tile_{local_x}_{local_y}"
                local_tile: Tile = Tile(id=tile_id, tile_type=TileType.OCEAN)

                # create tile
                await self.tiledao.post(world_id=world_id, island_id=island_id, tile=local_tile)
                msg: str = f"({tile_id}) brought into existence as {TileType.OCEAN}"
                logger.debug(msg)

                # Update the island --

                # get
                wrapped_island: WrappedData[IslandLite] = await self.islanddao.get(
                    world_id=world_id, island_id=island_id
                )

                # Patch - Add tile_id to in-memory representation before storing
                wrapped_island.data.tile_ids.add(tile_id)

                # put -- store island update (tile addition)
                await self.islanddao.put_safe(world_id=world_id, wrapped_island=wrapped_island)

        # 2. connect the tiles (nXm)
        wrapped_island: WrappedData[IslandLite] = await self.islanddao.get(world_id=world_id, island_id=island_id)
        for x in range(range_x_min, range_x_max):
            for y in range(range_y_min, range_y_max):
                local_x = x + 1
                local_y = y + 1
                tile_id: str = f"tile_{local_x}_{local_y}"
                msg: str = f"binding ({tile_id}) physically to peers"
                logger.debug(msg)

                # Bind LEFT
                target_tile_id: str = f"tile_{local_x - 1}_{local_y}"
                if target_tile_id in wrapped_island.data.tile_ids:
                    # load tile
                    local_tile: WrappedData[Tile] = await self.tiledao.get(
                        world_id=world_id, island_id=wrapped_island.data.id, tile_id=tile_id
                    )

                    # update tile
                    local_tile.data.next[TileConnectionType.LEFT] = target_tile_id
                    msg: str = (
                        f"tile {tile_id} -> {TileConnectionType.LEFT} -> {local_tile.data.next[TileConnectionType.LEFT]}"
                    )
                    logger.debug(msg)

                    # store tile
                    await self.tiledao.put_safe(
                        world_id=world_id, island_id=wrapped_island.data.id, wrapped_tile=local_tile
                    )

                # Bind RIGHT
                target_tile_id: str = f"tile_{local_x + 1}_{local_y}"
                if target_tile_id in wrapped_island.data.tile_ids:
                    # load tile
                    local_tile: WrappedData[Tile] = await self.tiledao.get(
                        world_id=world_id, island_id=wrapped_island.data.id, tile_id=tile_id
                    )

                    # update tile
                    local_tile.data.next[TileConnectionType.RIGHT] = target_tile_id

                    msg: str = (
                        f"tile {tile_id} -> {TileConnectionType.RIGHT} -> {local_tile.data.next[TileConnectionType.RIGHT]}"
                    )
                    logger.debug(msg)

                    # store tile
                    await self.tiledao.put_safe(
                        world_id=world_id, island_id=wrapped_island.data.id, wrapped_tile=local_tile
                    )

                # Bind UP
                target_tile_id: str = f"tile_{local_x}_{local_y - 1}"
                if target_tile_id in wrapped_island.data.tile_ids:
                    # load tile
                    local_tile: WrappedData[Tile] = await self.tiledao.get(
                        world_id=world_id, island_id=wrapped_island.data.id, tile_id=tile_id
                    )

                    # update tile
                    local_tile.data.next[TileConnectionType.UP] = target_tile_id
                    msg: str = (
                        f"tile {tile_id} -> {TileConnectionType.UP} -> {local_tile.data.next[TileConnectionType.UP]}"
                    )
                    logger.debug(msg)

                    # store tile
                    await self.tiledao.put_safe(
                        world_id=world_id, island_id=wrapped_island.data.id, wrapped_tile=local_tile
                    )

                # Bind DOWN
                target_tile_id: str = f"tile_{local_x}_{local_y + 1}"
                if target_tile_id in wrapped_island.data.tile_ids:
                    # load tile
                    local_tile: WrappedData[Tile] = await self.tiledao.get(
                        world_id=world_id, island_id=wrapped_island.data.id, tile_id=tile_id
                    )

                    # update tile
                    local_tile.data.next[TileConnectionType.DOWN] = target_tile_id
                    msg: str = (
                        f"tile {tile_id} -> {TileConnectionType.DOWN} -> {local_tile.data.next[TileConnectionType.DOWN]}"
                    )
                    logger.debug(msg)

                    # store tile
                    await self.tiledao.put_safe(
                        world_id=world_id, island_id=wrapped_island.data.id, wrapped_tile=local_tile
                    )

    async def create(self, world_id: str, name: str | None, dimensions: tuple[int, int], biome: TileType) -> IslandLite:
        if name is None:
            name = "roshar"

        # 1. blank, named island
        island: IslandLite = IslandLite(id=str(uuid.uuid4()), name=name, dimensions=dimensions, biome=biome)
        await self.islanddao.post(world_id=world_id, island=island)
        # island: Island = Island(id=str(uuid.uuid4()), name=name, dimensions=dimensions, biome=biome)

        # Define the maximum size
        max_x, max_y = dimensions

        # Generate an empty 2D block of ocean
        window: Window = Window(min=Coordinate(x=1, y=1), max=Coordinate(x=max_x, y=max_y))

        await self.generate_ocean_block(world_id=world_id, island_id=island.id, window=window)

        # Apply our terrain generation
        window = Window(min=Coordinate(x=2, y=2), max=Coordinate(x=max_x - 1, y=max_y - 1))

        await self.tiles_process(world_id=world_id, island=island, window=window)

        # get final state and return
        return (await self.islanddao.get(world_id=world_id, island_id=island.id)).data
