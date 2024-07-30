import logging
import secrets
import uuid

from ...contracts.dtos.island import Island
from ...contracts.dtos.tile import Tile
from ...contracts.types.connection import TileConnectionType
from ...contracts.types.tile import TileType

logger = logging.getLogger()


class FlatLandFactory:
    # pylint: disable=too-many-branches
    @staticmethod
    def generate(dim: tuple[int, int], biome: TileType) -> Island:

        # 1. blank, named island
        local_island: Island = Island(id=str(uuid.uuid4()), name="roshar", dim=dim)

        # 2. build a blank nXm island with water
        max_x, max_y = dim
        for x in range(0, max_x):
            for y in range(0, max_y):
                local_tile_name: str = f"tile_{x}_{y}"
                local_tile: Tile = Tile(id=local_tile_name, tile_type=TileType.WATER)
                local_island.tiles[local_tile.id] = local_tile

        # 3. connect the tiles (n,m)
        for x in range(0, max_x):
            for y in range(0, max_y):
                local_tile_name: str = f"tile_{x}_{y}"

                if f"tile_{x - 1}_{y}" in local_island.tiles:
                    local_island.tiles[local_tile_name].next[TileConnectionType.LEFT] = f"tile_{x - 1}_{y}"

                if f"tile_{x + 1}_{y}" in local_island.tiles:
                    local_island.tiles[local_tile_name].next[TileConnectionType.RIGHT] = f"tile_{x + 1}_{y}"

                if f"tile_{x}_{y - 1}" in local_island.tiles:
                    local_island.tiles[local_tile_name].next[TileConnectionType.UP] = f"tile_{x}_{y - 1}"

                if f"tile_{x}_{y + 1}" in local_island.tiles:
                    local_island.tiles[local_tile_name].next[TileConnectionType.DOWN] = f"tile_{x}_{y + 1}"

        # 4. set tile types
        # outer water
        for x in range(0, max_x):
            for y in range(0, max_y):
                if x in [0, max_x - 1] or y in [0, max_y - 1]:
                    local_tile_name: str = f"tile_{x}_{y}"
                    local_island.tiles[local_tile_name].tile_type = TileType.WATER

        # # 5. build shore and dirt
        # for x in range(0, max_x):
        #     for y in range(0, max_y):
        #         local_tile_name: str = f"tile_{x}_{y}"
        #         if local_island.tiles[local_tile_name].tile_type == TileType.UNKNOWN:
        #             msg: str = f"{local_tile_name}, type: {local_island.tiles[local_tile_name].tile_type}"
        #             logger.debug(msg)
        #             for connect_type, adjacent_id in local_island.tiles[local_tile_name].next.items():
        #                 # pylint: disable=line-too-long
        #                 msg: str = (
        #                     f"    direction: {connect_type}, adjacent_id: {adjacent_id}, type: {local_island.tiles[adjacent_id].tile_type}"
        #                 )
        #                 logger.debug(msg)
        #                 if local_island.tiles[adjacent_id].tile_type == TileType.WATER:
        #                     logger.debug("    water, we are shore, stopping ...")
        #                     local_island.tiles[local_tile_name].tile_type = TileType.SHORE
        #                     break
        #             # see if we got assigned shore..
        #             if local_island.tiles[local_tile_name].tile_type == TileType.UNKNOWN:
        #                 logger.debug("    still have undecided tile type .. (making biome type)")
        #                 local_island.tiles[local_tile_name].tile_type = biome

        # 5. randomally seed dirt
        # for x in range(0, max_x):
        #     for y in range(0, max_y):
        #         local_tile_name: str = f"tile_{x}_{y}"

        # 5. Apply random noise
        SPAWN_RATE: int = 90  # [30/100]
        SPAWN_TYPE: TileType = biome  # TileType.DIRT
        for x in range(1, max_x - 1):
            for y in range(1, max_y - 1):
                if secrets.randbelow(100) <= SPAWN_RATE:
                    # then we spawn the tile type
                    local_tile_name: str = f"tile_{x}_{y}"
                    local_island.tiles[local_tile_name].tile_type = SPAWN_TYPE

        # 6. Create Shore
        for x in range(0, max_x):
            for y in range(0, max_y):
                local_tile_name: str = f"tile_{x}_{y}"

                # for tiles what are solid, TileType.SHORE is rechecked here... do we want to long term?
                if local_island.tiles[local_tile_name].tile_type not in [TileType.UNKNOWN, TileType.WATER]:
                    next_to_water: bool = False
                    for _, adjecent_id in local_island.tiles[local_tile_name].next.items():
                        if local_island.tiles[adjecent_id].tile_type == TileType.WATER:
                            next_to_water = True
                            break
                    if next_to_water:
                        local_island.tiles[local_tile_name].tile_type = TileType.SHORE

        return local_island
