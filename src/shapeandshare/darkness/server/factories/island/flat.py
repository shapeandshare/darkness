import logging
import secrets
import uuid

from .... import WrappedData
from ....sdk.contracts.dtos.coordinate import Coordinate
from ....sdk.contracts.dtos.island_lite import IslandLite
from ....sdk.contracts.dtos.tile import Tile
from ....sdk.contracts.dtos.window import Window
from ....sdk.contracts.types.connection import TileConnectionType
from ....sdk.contracts.types.tile import TileType
from ...dao.tile import TileDao
from .abstract import AbstractIslandFactory

logger = logging.getLogger()


class FlatIslandFactory(AbstractIslandFactory):
    tiledao: TileDao

    def tiles_process(self, world_id: str, island: IslandLite, window: Window) -> None:
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
                # print(tile_id)

                # Mutate tiles to biome default (or dirt)
                self.mutate_tile(
                    world_id=world_id,
                    island=island,
                    tile_id=tile_id,
                    mutate=90,  # percentage of 100%
                    type=(island.biome if island.biome else TileType.DIRT),
                )

        # Add Eradicates (rocks)
        for x in range(range_x_min, range_x_max):
            for y in range(range_y_min, range_y_max):
                local_x = x + 1
                local_y = y + 1
                tile_id: str = f"tile_{local_x}_{local_y}"
                # print(tile_id)
                self.mutate_tile(
                    world_id=world_id,
                    island=island,
                    tile_id=tile_id,
                    mutate=0.5,  # 0.5% change (very low)
                    type=TileType.ROCK,
                )

        # TODO: isolated ocean is NOT ocean, we MUST have path to the edge
        # Convert inner Ocean to Water Tiles
        for x in range(range_x_min, range_x_max):
            for y in range(range_y_min, range_y_max):
                local_x = x + 1
                local_y = y + 1
                tile_id: str = f"tile_{local_x}_{local_y}"
                # print(tile_id)

                # Convert inner Ocean to Water Tiles
                self.brackish_tile(world_id=world_id, island=island, tile_id=tile_id)

        # Erode Tiles (to make shore)
        for x in range(range_x_min, range_x_max):
            for y in range(range_y_min, range_y_max):
                local_x = x + 1
                local_y = y + 1
                tile_id: str = f"tile_{local_x}_{local_y}"
                # print(tile_id)

                # Erode Tiles
                self.erode_tile(world_id=world_id, island=island, tile_id=tile_id)

        # Grow Tiles
        for x in range(range_x_min, range_x_max):
            for y in range(range_y_min, range_y_max):
                local_x = x + 1
                local_y = y + 1
                tile_id: str = f"tile_{local_x}_{local_y}"
                # print(tile_id)

                # Grow Tiles
                self.grow_tile(world_id=world_id, island=island, tile_id=tile_id)

    def mutate_tile(self, world_id: str, island: IslandLite, tile_id: str, mutate: float, type: TileType) -> None:
        if secrets.randbelow(100) <= mutate:
            # then we spawn the tile type
            # island.tiles[tile_id].tile_type = type

            # We don't current have a patch, so get and put..
            # get
            target_tile: WrappedData[Tile] = self.tiledao.get(world_id=world_id, island_id=island.id, tile_id=tile_id)
            # patch
            target_tile.data.tile_type = type
            # put
            self.tiledao.put_safe(world_id=world_id, island_id=island.id, wrapped_tile=target_tile)
            # self.tiledao.put(world_id=world_id, island_id=island.id, tile=target_tile.data)

    def convert_tile(self, world_id: str, island: IslandLite, tile_id: str, source: TileType, target: TileType) -> None:
        # get
        target_tile: WrappedData[Tile] = self.tiledao.get(world_id=world_id, island_id=island.id, tile_id=tile_id)

        # check
        if target_tile.data.tile_type == source:
            # patch
            target_tile.data.tile_type = target

            # put
            self.tiledao.put_safe(world_id=world_id, island_id=island.id, wrapped_tile=target_tile)
            # self.tiledao.put(world_id=world_id, island_id=island.id, tile=target_tile.data)

    def adjecent_liquids(self, world_id: str, island: IslandLite, tile_id: str) -> list[TileType]:
        return self.adjecent_to(
            world_id=world_id, island=island, tile_id=tile_id, types=[TileType.OCEAN, TileType.WATER]
        )

    def adjecent_to(
        self, world_id: str, island: IslandLite, tile_id: str, types: list[TileType] | None
    ) -> list[TileType]:
        adjecent_targets: list[TileType] = []

        target_tile: WrappedData[Tile] = self.tiledao.get(world_id=world_id, island_id=island.id, tile_id=tile_id)
        for _, adjecent_id in target_tile.data.next.items():
            # assert adjecent_id == island.tiles[adjecent_id].id
            # print(f"tile {tile_id} -> {adjecent_dir} -> {adjecent_id}:{island.tiles[adjecent_id].id} -> {island.tiles[adjecent_id].tile_type}")

            adjecent_tile: WrappedData[Tile] = self.tiledao.get(
                world_id=world_id, island_id=island.id, tile_id=adjecent_id
            )
            if adjecent_tile.data.tile_type in types and adjecent_tile.data.tile_type not in adjecent_targets:
                adjecent_targets.append(adjecent_tile.data.tile_type)
        # print(f"tile {tile_id} is adjecent to: {adjecent_targets}")
        return adjecent_targets

    def grow_tile(self, world_id: str, island: IslandLite, tile_id: str) -> None:
        # if island.tiles[tile_id].tile_type not in [TileType.UNKNOWN, TileType.OCEAN, TileType.WATER]:

        # get
        target_tile: WrappedData[Tile] = self.tiledao.get(world_id=world_id, island_id=island.id, tile_id=tile_id)

        # dirt -> grass
        if target_tile.data.tile_type == TileType.DIRT:
            adjecent_liquids: list[TileType] = self.adjecent_liquids(world_id=world_id, island=island, tile_id=tile_id)
            if TileType.WATER in adjecent_liquids and TileType.OCEAN not in adjecent_liquids:
                # patch
                target_tile.data.tile_type = TileType.GRASS

                # put
                self.tiledao.put_safe(world_id=world_id, island_id=island.id, wrapped_tile=target_tile)
                # self.tiledao.put(world_id=world_id, island_id=island.id, tile=target_tile.data)

        # grass+water (no dirt/ocean) -> forest
        if target_tile.data.tile_type == TileType.GRASS:
            neighbors: list[TileType] = self.adjecent_to(
                world_id=world_id,
                island=island,
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
                self.tiledao.put_safe(world_id=world_id, island_id=island.id, wrapped_tile=target_tile)
                # self.tiledao.put(world_id=world_id, island_id=island.id, tile=target_tile.data)

        # # grass+(dirt)
        # if island.tiles[tile_id].tile_type == TileType.GRASS:
        #     neighbors: list[TileType] = FlatIslandFactory.adjecent_to(
        #         # TODO: review this josh ...
        #         island=island, tile_id=tile_id, types=[TileType.WATER, TileType.GRASS, TileType.DIRT, TileType.FOREST]
        #     )

    def brackish_tile(self, world_id: str, island: IslandLite, tile_id: str):
        # Convert inner Ocean to Water Tiles

        # See if we are next to ocean
        neighbors: list[TileType] = self.adjecent_to(
            world_id=world_id, island=island, tile_id=tile_id, types=[TileType.OCEAN]
        )
        if len(neighbors) < 1:
            self.convert_tile(
                world_id=world_id, island=island, tile_id=tile_id, source=TileType.OCEAN, target=TileType.WATER
            )

    def erode_tile(self, world_id: str, island: IslandLite, tile_id: str) -> None:
        # get
        target_tile: WrappedData[Tile] = self.tiledao.get(world_id=world_id, island_id=island.id, tile_id=tile_id)

        # shore erosion
        if target_tile.data.tile_type not in [TileType.UNKNOWN, TileType.OCEAN, TileType.WATER, TileType.SHORE]:
            adjecent_liquids: list[TileType] = self.adjecent_liquids(world_id=world_id, island=island, tile_id=tile_id)
            # Apply erosion - rocks and be left by oceans, everything else becomes shore
            if TileType.OCEAN in adjecent_liquids:
                if target_tile.data.tile_type not in (TileType.ROCK, TileType.SHORE):
                    # previous_type = target_tile.tile_type

                    # patch
                    target_tile.data.tile_type = TileType.SHORE

                    # put
                    self.tiledao.put_safe(world_id=world_id, island_id=island.id, wrapped_tile=target_tile)
                    # self.tiledao.put(world_id=world_id, island_id=island.id, tile=target_tile.data)

                    # print(f"tile {tile_id}:{previous_type} converted to {TileType.SHORE}")

    def generate_ocean_block(self, world_id: str, island: IslandLite, window: Window):
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

                # store tile
                self.tiledao.post(world_id=world_id, island_id=island.id, tile=local_tile)
                logger.debug(f"({tile_id}) brought into existence as {TileType.OCEAN}")

                # Add tile_id to in-memory representation before storing
                island.tile_ids.add(tile_id)

                # store island update (tile addition)
                self.islanddao.put(world_id=world_id, island=island)

        # 2. connect the tiles (nXm)
        for x in range(range_x_min, range_x_max):
            for y in range(range_y_min, range_y_max):
                local_x = x + 1
                local_y = y + 1
                tile_id: str = f"tile_{local_x}_{local_y}"
                logger.debug(f"binding ({tile_id}) physically to peers")

                target_tile_id: str = f"tile_{local_x - 1}_{local_y}"
                if target_tile_id in island.tile_ids:
                    # load tile
                    local_tile: WrappedData[Tile] = self.tiledao.get(
                        world_id=world_id, island_id=island.id, tile_id=target_tile_id
                    )

                    # update tile
                    local_tile.data.next[TileConnectionType.LEFT] = f"tile_{local_x - 1}_{local_y}"
                    logger.debug(
                        f"tile {tile_id} -> {TileConnectionType.LEFT} -> {local_tile.data.next[TileConnectionType.LEFT]}"
                    )

                    # store tile
                    self.tiledao.put_safe(world_id=world_id, island_id=island.id, wrapped_tile=local_tile)
                    # self.tiledao.put(world_id=world_id, island_id=island.id, tile=local_tile.data)

                target_tile_id: str = f"tile_{local_x + 1}_{local_y}"
                if target_tile_id in island.tile_ids:
                    # load tile
                    local_tile: WrappedData[Tile] = self.tiledao.get(
                        world_id=world_id, island_id=island.id, tile_id=target_tile_id
                    )

                    # update tile
                    local_tile.data.next[TileConnectionType.RIGHT] = f"tile_{local_x + 1}_{local_y}"

                    logger.debug(
                        f"tile {tile_id} -> {TileConnectionType.RIGHT} -> {local_tile.data.next[TileConnectionType.RIGHT]}"
                    )

                    # store tile
                    self.tiledao.put_safe(world_id=world_id, island_id=island.id, wrapped_tile=local_tile)
                    # self.tiledao.put(world_id=world_id, island_id=island.id, tile=local_tile.data)

                target_tile_id: str = f"tile_{local_x}_{local_y - 1}"
                if target_tile_id in island.tile_ids:
                    # load tile
                    local_tile: WrappedData[Tile] = self.tiledao.get(
                        world_id=world_id, island_id=island.id, tile_id=target_tile_id
                    )

                    # update tile
                    local_tile.data.next[TileConnectionType.UP] = f"tile_{local_x}_{local_y - 1}"
                    logger.debug(
                        f"tile {tile_id} -> {TileConnectionType.UP} -> {local_tile.data.next[TileConnectionType.UP]}"
                    )

                    # store tile
                    self.tiledao.put_safe(world_id=world_id, island_id=island.id, wrapped_tile=local_tile)
                    # self.tiledao.put(world_id=world_id, island_id=island.id, tile=local_tile.data)

                target_tile_id: str = f"tile_{local_x}_{local_y + 1}"
                if target_tile_id in island.tile_ids:
                    # load tile
                    local_tile: WrappedData[Tile] = self.tiledao.get(
                        world_id=world_id, island_id=island.id, tile_id=target_tile_id
                    )

                    # update tile
                    local_tile.data.next[TileConnectionType.DOWN] = f"tile_{local_x}_{local_y + 1}"
                    logger.debug(
                        f"tile {tile_id} -> {TileConnectionType.DOWN} -> {local_tile.data.next[TileConnectionType.DOWN]}"
                    )

                    # store tile
                    self.tiledao.put_safe(world_id=world_id, island_id=island.id, wrapped_tile=local_tile)
                    # self.tiledao.put(world_id=world_id, island_id=island.id, tile=local_tile.data)

    def create(self, world_id: str, name: str | None, dimensions: tuple[int, int], biome: TileType) -> IslandLite:
        if name is None:
            name = "roshar"

        # 1. blank, named island
        island: IslandLite = IslandLite(id=str(uuid.uuid4()), name=name, dimensions=dimensions, biome=biome)
        self.islanddao.post(world_id=world_id, island=island)
        # island: Island = Island(id=str(uuid.uuid4()), name=name, dimensions=dimensions, biome=biome)

        # Define the maximum size
        max_x, max_y = dimensions

        # Generate an empty 2D block of ocean
        window: Window = Window(min=Coordinate(x=1, y=1), max=Coordinate(x=max_x, y=max_y))
        # print(window.model_dump_json())
        self.generate_ocean_block(world_id=world_id, island=island, window=window)

        # Apply our terrain generation
        window = Window(min=Coordinate(x=2, y=2), max=Coordinate(x=max_x - 1, y=max_y - 1))
        # print(window.model_dump_json())
        self.tiles_process(world_id=world_id, island=island, window=window)

        return island
