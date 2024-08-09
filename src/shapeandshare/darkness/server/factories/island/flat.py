import logging
import secrets
import uuid

from ....sdk.contracts.dtos.coordinate import Coordinate
from ....sdk.contracts.dtos.island import Island
from ....sdk.contracts.dtos.tile import Tile
from ....sdk.contracts.dtos.window import Window
from ....sdk.contracts.types.connection import TileConnectionType
from ....sdk.contracts.types.tile import TileType

logger = logging.getLogger()


class FlatIslandFactory:

    @staticmethod
    def tiles_process(island: Island, window: Window) -> None:
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
                FlatIslandFactory.mutate_tile(
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
                FlatIslandFactory.mutate_tile(island=island, tile_id=tile_id, mutate=0.5, type=TileType.ROCK)

        # TODO: isolated ocean is NOT ocean, we MUST have path to the edge
        # Convert inner Ocean to Water Tiles
        for x in range(range_x_min, range_x_max):
            for y in range(range_y_min, range_y_max):
                local_x = x + 1
                local_y = y + 1
                tile_id: str = f"tile_{local_x}_{local_y}"
                # print(tile_id)

                # Convert inner Ocean to Water Tiles
                FlatIslandFactory.brackish_tile(island=island, tile_id=tile_id)

        # Erode Tiles (to make shore)
        for x in range(range_x_min, range_x_max):
            for y in range(range_y_min, range_y_max):
                local_x = x + 1
                local_y = y + 1
                tile_id: str = f"tile_{local_x}_{local_y}"
                # print(tile_id)

                # Erode Tiles
                FlatIslandFactory.erode_tile(island=island, tile_id=tile_id)

        # Grow Tiles
        for x in range(range_x_min, range_x_max):
            for y in range(range_y_min, range_y_max):
                local_x = x + 1
                local_y = y + 1
                tile_id: str = f"tile_{local_x}_{local_y}"
                # print(tile_id)

                # Grow Tiles
                FlatIslandFactory.grow_tile(island=island, tile_id=tile_id)

    @staticmethod
    def mutate_tile(island: Island, tile_id: str, mutate: float, type: TileType) -> None:
        if secrets.randbelow(100) <= mutate:
            # then we spawn the tile type
            island.tiles[tile_id].tile_type = type

    @staticmethod
    def convert_tile(island: Island, tile_id: str, source: TileType, target: TileType) -> None:
        if tile_id in island.tiles and island.tiles[tile_id].tile_type == source:
            island.tiles[tile_id].tile_type = target

    @staticmethod
    def adjecent_liquids(island: Island, tile_id: str) -> list[TileType]:
        return FlatIslandFactory.adjecent_to(island=island, tile_id=tile_id, types=[TileType.OCEAN, TileType.WATER])

    @staticmethod
    def adjecent_to(island: Island, tile_id: str, types: list[TileType] | None) -> list[TileType]:
        adjecent_targets: list[TileType] = []
        for adjecent_dir, adjecent_id in island.tiles[tile_id].next.items():
            # assert adjecent_id == island.tiles[adjecent_id].id
            # print(f"tile {tile_id} -> {adjecent_dir} -> {adjecent_id}:{island.tiles[adjecent_id].id} -> {island.tiles[adjecent_id].tile_type}")
            if (
                island.tiles[adjecent_id].tile_type in types
                and island.tiles[adjecent_id].tile_type not in adjecent_targets
            ):
                adjecent_targets.append(island.tiles[adjecent_id].tile_type)
        # print(f"tile {tile_id} is adjecent to: {adjecent_targets}")
        return adjecent_targets

    @staticmethod
    def grow_tile(island: Island, tile_id: str) -> None:
        # if island.tiles[tile_id].tile_type not in [TileType.UNKNOWN, TileType.OCEAN, TileType.WATER]:

        # dirt -> grass
        if island.tiles[tile_id].tile_type == TileType.DIRT:
            adjecent_liquids: list[TileType] = FlatIslandFactory.adjecent_liquids(island=island, tile_id=tile_id)
            if TileType.WATER in adjecent_liquids and TileType.OCEAN not in adjecent_liquids:
                island.tiles[tile_id].tile_type = TileType.GRASS

        # grass+water (no dirt/ocean) -> forest
        if island.tiles[tile_id].tile_type == TileType.GRASS:
            neighbors: list[TileType] = FlatIslandFactory.adjecent_to(
                island=island, tile_id=tile_id, types=[TileType.WATER, TileType.GRASS, TileType.OCEAN]
            )

            # no forests grow by oceans
            if TileType.OCEAN in neighbors:
                return

            if len(neighbors) > 1:
                # next to more than one kind (grass/water)
                island.tiles[tile_id].tile_type = TileType.FOREST

        # # grass+(dirt)
        # if island.tiles[tile_id].tile_type == TileType.GRASS:
        #     neighbors: list[TileType] = FlatIslandFactory.adjecent_to(
        #         # TODO: review this josh ...
        #         island=island, tile_id=tile_id, types=[TileType.WATER, TileType.GRASS, TileType.DIRT, TileType.FOREST]
        #     )

    @staticmethod
    def brackish_tile(island: Island, tile_id: str):
        # Convert inner Ocean to Water Tiles

        # See if we are next to ocean
        neighbors: list[TileType] = FlatIslandFactory.adjecent_to(
            island=island, tile_id=tile_id, types=[TileType.OCEAN]
        )
        if len(neighbors) < 1:
            FlatIslandFactory.convert_tile(island=island, tile_id=tile_id, source=TileType.OCEAN, target=TileType.WATER)

    @staticmethod
    def erode_tile(island: Island, tile_id: str) -> None:
        # shore erosion
        if island.tiles[tile_id].tile_type not in [TileType.UNKNOWN, TileType.OCEAN, TileType.WATER, TileType.SHORE]:
            adjecent_liquids: list[TileType] = FlatIslandFactory.adjecent_liquids(island=island, tile_id=tile_id)
            # Apply erosion - rocks and be left by oceans, everything else becomes shore
            if TileType.OCEAN in adjecent_liquids:
                if island.tiles[tile_id].tile_type not in (TileType.ROCK, TileType.SHORE):
                    previous_type = island.tiles[tile_id].tile_type
                    island.tiles[tile_id].tile_type = TileType.SHORE
                    # print(f"tile {tile_id}:{previous_type} converted to {TileType.SHORE}")

    @staticmethod
    def generate_ocean_block(island: Island, window: Window):
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
                logger.debug(f"({tile_id}) brought into existence as {TileType.OCEAN}")

                local_tile: Tile = Tile(id=tile_id, tile_type=TileType.OCEAN)
                island.tiles[local_tile.id] = local_tile

        # 2. connect the tiles (nXm)
        for x in range(range_x_min, range_x_max):
            for y in range(range_y_min, range_y_max):
                local_x = x + 1
                local_y = y + 1
                tile_id: str = f"tile_{local_x}_{local_y}"
                logger.debug(f"binding ({tile_id}) physically to peers")

                if f"tile_{local_x - 1}_{local_y}" in island.tiles:
                    island.tiles[tile_id].next[TileConnectionType.LEFT] = f"tile_{local_x - 1}_{local_y}"
                    logger.debug(
                        f"tile {tile_id} -> {TileConnectionType.LEFT} -> {island.tiles[tile_id].next[TileConnectionType.LEFT]}"
                    )

                if f"tile_{local_x + 1}_{local_y}" in island.tiles:
                    island.tiles[tile_id].next[TileConnectionType.RIGHT] = f"tile_{local_x + 1}_{local_y}"
                    logger.debug(
                        f"tile {tile_id} -> {TileConnectionType.RIGHT} -> {island.tiles[tile_id].next[TileConnectionType.RIGHT]}"
                    )

                if f"tile_{local_x}_{local_y - 1}" in island.tiles:
                    island.tiles[tile_id].next[TileConnectionType.UP] = f"tile_{local_x}_{local_y - 1}"
                    logger.debug(
                        f"tile {tile_id} -> {TileConnectionType.UP} -> {island.tiles[tile_id].next[TileConnectionType.UP]}"
                    )

                if f"tile_{local_x}_{local_y + 1}" in island.tiles:
                    island.tiles[tile_id].next[TileConnectionType.DOWN] = f"tile_{local_x}_{local_y + 1}"
                    logger.debug(
                        f"tile {tile_id} -> {TileConnectionType.DOWN} -> {island.tiles[tile_id].next[TileConnectionType.DOWN]}"
                    )

    @staticmethod
    def generate(dimensions: tuple[int, int], biome: TileType, name: str | None = None) -> Island:
        if name is None:
            name = "roshar"

        # 1. blank, named island
        island: Island = Island(id=str(uuid.uuid4()), name=name, dimensions=dimensions, biome=biome)

        # Define the maximum size
        max_x, max_y = dimensions

        # Generate an empty 2D block of ocean
        window: Window = Window(min=Coordinate(x=1, y=1), max=Coordinate(x=max_x, y=max_y))
        # print(window.model_dump_json())
        FlatIslandFactory.generate_ocean_block(island=island, window=window)

        # Apply our terrain generation
        window = Window(min=Coordinate(x=2, y=2), max=Coordinate(x=max_x - 1, y=max_y - 1))
        # print(window.model_dump_json())
        FlatIslandFactory.tiles_process(island=island, window=window)

        return island
