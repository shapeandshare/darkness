import uuid
from ...contracts.dtos.island import Island
from ...contracts.dtos.tile import Tile
from ...contracts.types.connection import TileConnectionType
from ...contracts.types.tile import TileType


class FlatIslandFactory:
    @staticmethod
    def flat(universal_dim: tuple[int, int], biome: TileType) -> Island:

        # 1. blank, named island
        localIsland: Island = Island(
            id=str(uuid.uuid4()),
            name="roshar"
        )

        # 2. build a blank nXm island
        max_x, max_y = universal_dim
        for x in range(0, max_x):
            for y in range(0, max_y):
                local_tile_name: str = f"tile_{x}_{y}"
                localTile: Tile = Tile(id=local_tile_name, tileType=TileType.unknown)
                localIsland.tiles[localTile.id] = localTile

        # 3. connect the tiles (n,m)
        for x in range(0, max_x):
            for y in range(0, max_y):
                local_tile_name: str = f"tile_{x}_{y}"

                if f"tile_{x - 1}_{y}" in localIsland.tiles:
                    localIsland.tiles[local_tile_name].next[
                        TileConnectionType.left] = f"tile_{x - 1}_{y}"

                if f"tile_{x + 1}_{y}" in localIsland.tiles:
                    localIsland.tiles[local_tile_name].next[
                        TileConnectionType.right] = f"tile_{x + 1}_{y}"

                if f"tile_{x}_{y - 1}" in localIsland.tiles:
                    localIsland.tiles[local_tile_name].next[
                        TileConnectionType.up] = f"tile_{x}_{y - 1}"

                if f"tile_{x}_{y + 1}" in localIsland.tiles:
                    localIsland.tiles[local_tile_name].next[
                        TileConnectionType.down] = f"tile_{x}_{y + 1}"

        # 4. set tile types

        # outer water
        for x in range(0, max_x):
            for y in range(0, max_y):
                if x in [0, max_x - 1] or y in [0, max_y - 1]:
                    local_tile_name: str = f"tile_{x}_{y}"
                    localIsland.tiles[local_tile_name].tileType = TileType.water

        # 5. build shore and dirt
        for x in range(0, max_x):
            for y in range(0, max_y):
                local_tile_name: str = f"tile_{x}_{y}"
                if localIsland.tiles[local_tile_name].tileType == TileType.unknown:
                    # print(f"{local_tile_name}, type: {localWorld.islands[localIsland.id].tiles[local_tile_name].tileType}")
                    for (connect_type, adjacent_id) in localIsland.tiles[local_tile_name].next.items():
                        # print(f"    direction: {connect_type}, adjacent_id: {adjacent_id}, type: {localWorld.islands[localIsland.id].tiles[adjacent_id].tileType}")
                        if localIsland.tiles[adjacent_id].tileType == TileType.water:
                            # print("    water, we are shore, stopping ...")
                            localIsland.tiles[local_tile_name].tileType = TileType.shore
                            break
                    # see if we got assigned shore..
                    if localIsland.tiles[local_tile_name].tileType == TileType.unknown:
                        # print("    still have undecided tile type .. (making it plain dirt)")
                        localIsland.tiles[local_tile_name].tileType = biome

        return localIsland
