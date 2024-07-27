import uuid

from darkness.dtos.contracts.island import Island
from darkness.dtos.contracts.tile import Tile
from darkness.dtos.contracts.types.connection import TileConnectionType
from darkness.dtos.contracts.types.tile import TileType
from darkness.dtos.contracts.world import World



def defaultWorld(universal_dim: tuple[int, int]) -> World:

    # 1. blank, named world
    localWorld: World = World(
        id=str(uuid.uuid4()),
        name="darkness",
    )

    # 2. blank, named island [define a single 5x5 island ]
    localIsland: Island = Island(
        id=str(uuid.uuid4()),
        name="roshar"
    )
    localWorld.islands[localIsland.id] = localIsland

    # 3. build a blank nXm island
    max_x, max_y = universal_dim
    for x in range(0, max_x):
        for y in range(0, max_y):
            local_tile_name: str = f"tile_{x}_{y}"
            localTile: Tile = Tile(id=local_tile_name, tileType=TileType.unknown)
            localWorld.islands[localIsland.id].tiles[localTile.id] = localTile

    # 4. connect the tiles (n,m)
    for x in range(0, max_x):
        for y in range(0, max_y):
            local_tile_name: str = f"tile_{x}_{y}"

            if f"tile_{x-1}_{y}" in localWorld.islands[localIsland.id].tiles:
                localWorld.islands[localIsland.id].tiles[local_tile_name].next[TileConnectionType.left] = f"tile_{x-1}_{y}"

            if f"tile_{x+1}_{y}" in localWorld.islands[localIsland.id].tiles:
                localWorld.islands[localIsland.id].tiles[local_tile_name].next[TileConnectionType.right] = f"tile_{x+1}_{y}"

            if f"tile_{x}_{y-1}" in localWorld.islands[localIsland.id].tiles:
                localWorld.islands[localIsland.id].tiles[local_tile_name].next[TileConnectionType.up] = f"tile_{x}_{y-1}"

            if f"tile_{x}_{y+1}" in localWorld.islands[localIsland.id].tiles:
                localWorld.islands[localIsland.id].tiles[local_tile_name].next[TileConnectionType.down] = f"tile_{x}_{y+1}"

    # 5. set tile types

    # outer water
    for x in range(0, max_x):
        for y in range(0, max_y):
            if x in [0, max_x-1] or y in [0, max_y-1]:
                local_tile_name: str = f"tile_{x}_{y}"
                localWorld.islands[localIsland.id].tiles[local_tile_name].tileType = TileType.water

    # build shore and dirt
    for x in range(0, max_x):
        for y in range(0, max_y):
            local_tile_name: str = f"tile_{x}_{y}"
            if localWorld.islands[localIsland.id].tiles[local_tile_name].tileType == TileType.unknown:
                # print(f"{local_tile_name}, type: {localWorld.islands[localIsland.id].tiles[local_tile_name].tileType}")
                for (connect_type, adjacent_id) in localWorld.islands[localIsland.id].tiles[local_tile_name].next.items():
                    # print(f"    direction: {connect_type}, adjacent_id: {adjacent_id}, type: {localWorld.islands[localIsland.id].tiles[adjacent_id].tileType}")
                    if localWorld.islands[localIsland.id].tiles[adjacent_id].tileType == TileType.water:
                        # print("    water, we are shore, stopping ...")
                        localWorld.islands[localIsland.id].tiles[local_tile_name].tileType = TileType.shore
                        break
                # see if we got assigned shore..
                if localWorld.islands[localIsland.id].tiles[local_tile_name].tileType == TileType.unknown:
                    # print("    still have undecided tile type .. (making it plain dirt)")
                    localWorld.islands[localIsland.id].tiles[local_tile_name].tileType = TileType.dirt


    return localWorld




    # print(universal_dim[0])
    # print(universal_dim[1])




    #
    #
    # ######################### define a single 5x5 island #########################
    # localIsland: Island = Island(
    #     name="roshar",
    #     id=str(uuid.uuid4()),
    #     tiles={
    #         # row 0
    #         tile_0_0.id: tile_0_0,
    #         tile_0_1.id: tile_0_1,
    #         tile_0_2.id: tile_0_2,
    #         tile_0_3.id: tile_0_3,
    #         tile_0_4.id: tile_0_4,
    #
    #         # row 1
    #         tile_1_0.id: tile_1_0,
    #         tile_1_1.id: tile_1_1,
    #         tile_1_2.id: tile_1_2,
    #         tile_1_3.id: tile_1_3,
    #         tile_1_4.id: tile_1_4,
    #
    #         # row 2
    #         tile_2_0.id: tile_2_0,
    #         tile_2_1.id: tile_2_1,
    #         tile_2_2.id: tile_2_2,
    #         tile_2_3.id: tile_2_3,
    #         tile_2_4.id: tile_2_4,
    #
    #         # row 3
    #         tile_3_0.id: tile_3_0,
    #         tile_3_1.id: tile_3_1,
    #         tile_3_2.id: tile_3_2,
    #         tile_3_3.id: tile_3_3,
    #         tile_3_4.id: tile_3_4,
    #
    #         # row 4
    #         tile_4_0.id: tile_4_0,
    #         tile_4_1.id: tile_4_1,
    #         tile_4_2.id: tile_4_2,
    #         tile_4_3.id: tile_4_3,
    #         tile_4_4.id: tile_4_4,
    #     }
    # )
    #
    #
    #
    #
    #
    #
    # ### build tiles #######################################################################################
    # # tile_x_y | (0,0) top left -- (x,y) -- bottom right
    #
    # ### column 0 ###########################################
    # tile_0_0: Tile = Tile(id="tile_0_0", tileType=TileType.water)
    # tile_0_1: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.water)
    # tile_0_2: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.water)
    # tile_0_3: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.water)
    # tile_0_4: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.water)
    #
    # ### column 1 ###########################################
    # tile_1_0: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.water)
    # tile_1_1: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.shore)
    # tile_1_2: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.shore)
    # tile_1_3: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.shore)
    # tile_1_4: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.water)
    #
    # ### column 2 ###########################################
    # tile_2_0: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.water)
    # tile_2_1: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.shore)
    # tile_2_2: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.dirt)
    # tile_2_3: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.shore)
    # tile_2_4: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.water)
    #
    # ### column 3 ###########################################
    # tile_3_0: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.water)
    # tile_3_1: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.shore)
    # tile_3_2: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.shore)
    # tile_3_3: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.shore)
    # tile_3_4: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.water)
    #
    # ### column 4 ###########################################
    # tile_4_0: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.water)
    # tile_4_1: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.water)
    # tile_4_2: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.water)
    # tile_4_3: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.water)
    # tile_4_4: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.water)
    #
    # ### connect tiles #######################################################################################
    #
    # ### column 0 ##############################################################################
    #
    # tile_0_0.next[TileConnectionType.right] = tile_1_0.id
    # tile_0_0.next[TileConnectionType.down] = tile_0_1.id
    #
    # tile_0_1.next[TileConnectionType.up] = tile_0_0.id
    # tile_0_1.next[TileConnectionType.right] = tile_1_1.id
    # tile_0_1.next[TileConnectionType.down] = tile_0_2.id
    #
    # tile_0_2.next[TileConnectionType.up] = tile_0_1.id
    # tile_0_2.next[TileConnectionType.right] = tile_1_2.id
    # tile_0_2.next[TileConnectionType.down] = tile_0_3.id
    #
    # tile_0_3.next[TileConnectionType.up] = tile_0_2.id
    # tile_0_3.next[TileConnectionType.right] = tile_1_3.id
    # tile_0_3.next[TileConnectionType.down] = tile_0_4.id
    #
    # tile_0_4.next[TileConnectionType.up] = tile_0_3.id
    # tile_0_4.next[TileConnectionType.right] = tile_1_4.id
    #
    # ### column 1 ##############################################################################
    #
    # tile_1_0.next[TileConnectionType.left] = tile_0_0.id
    # tile_1_0.next[TileConnectionType.right] = tile_2_0.id
    # tile_1_0.next[TileConnectionType.down] = tile_1_1.id
    #
    # tile_1_1.next[TileConnectionType.left] = tile_0_1.id
    # tile_1_1.next[TileConnectionType.right] = tile_2_1.id
    # tile_1_1.next[TileConnectionType.up] = tile_1_0.id
    # tile_1_1.next[TileConnectionType.down] = tile_1_2.id
    #
    # tile_1_2.next[TileConnectionType.left] = tile_0_2.id
    # tile_1_2.next[TileConnectionType.right] = tile_2_2.id
    # tile_1_2.next[TileConnectionType.up] = tile_1_1.id
    # tile_1_2.next[TileConnectionType.down] = tile_1_3.id
    #
    # tile_1_3.next[TileConnectionType.left] = tile_0_3.id
    # tile_1_3.next[TileConnectionType.right] = tile_2_3.id
    # tile_1_3.next[TileConnectionType.up] = tile_1_2.id
    # tile_1_3.next[TileConnectionType.down] = tile_1_4.id
    #
    # tile_1_4.next[TileConnectionType.left] = tile_0_4.id
    # tile_1_4.next[TileConnectionType.right] = tile_2_4.id
    # tile_1_4.next[TileConnectionType.up] = tile_1_3.id
    #
    # ### column 2 ##############################################################################
    #
    # tile_2_0.next[TileConnectionType.left] = tile_1_0.id
    # tile_2_0.next[TileConnectionType.right] = tile_3_0.id
    # tile_2_0.next[TileConnectionType.down] = tile_2_1.id
    #
    # tile_2_1.next[TileConnectionType.left] = tile_1_1.id
    # tile_2_1.next[TileConnectionType.right] = tile_3_1.id
    # tile_2_1.next[TileConnectionType.up] = tile_2_0.id
    # tile_2_1.next[TileConnectionType.down] = tile_2_2.id
    #
    # tile_2_2.next[TileConnectionType.left] = tile_1_2.id
    # tile_2_2.next[TileConnectionType.right] = tile_3_2.id
    # tile_2_2.next[TileConnectionType.up] = tile_2_1.id
    # tile_2_2.next[TileConnectionType.down] = tile_2_3.id
    #
    # tile_2_3.next[TileConnectionType.left] = tile_1_3.id
    # tile_2_3.next[TileConnectionType.right] = tile_3_3.id
    # tile_2_3.next[TileConnectionType.up] = tile_2_2.id
    # tile_2_3.next[TileConnectionType.down] = tile_2_4.id
    #
    # tile_2_4.next[TileConnectionType.left] = tile_1_4.id
    # tile_2_4.next[TileConnectionType.right] = tile_3_4.id
    # tile_2_4.next[TileConnectionType.up] = tile_2_3.id
    #
    # ### column 3 ##############################################################################
    #
    # tile_3_0.next[TileConnectionType.left] = tile_2_0.id
    # tile_3_0.next[TileConnectionType.right] = tile_4_0.id
    # tile_3_0.next[TileConnectionType.down] = tile_3_1.id
    #
    # tile_3_1.next[TileConnectionType.left] = tile_2_1.id
    # tile_3_1.next[TileConnectionType.right] = tile_4_1.id
    # tile_3_1.next[TileConnectionType.up] = tile_3_0.id
    # tile_3_1.next[TileConnectionType.down] = tile_3_2.id
    #
    # tile_3_2.next[TileConnectionType.left] = tile_2_2.id
    # tile_3_2.next[TileConnectionType.right] = tile_4_2.id
    # tile_3_2.next[TileConnectionType.up] = tile_3_1.id
    # tile_3_2.next[TileConnectionType.down] = tile_3_3.id
    #
    # tile_3_3.next[TileConnectionType.left] = tile_2_3.id
    # tile_3_3.next[TileConnectionType.right] = tile_4_3.id
    # tile_3_3.next[TileConnectionType.up] = tile_3_2.id
    # tile_3_3.next[TileConnectionType.down] = tile_3_4.id
    #
    # tile_3_4.next[TileConnectionType.left] = tile_2_4.id
    # tile_3_4.next[TileConnectionType.right] = tile_4_4.id
    # tile_3_4.next[TileConnectionType.up] = tile_3_3.id
    #
    # ### column 4 ##############################################################################
    #
    # tile_4_0.next[TileConnectionType.left] = tile_3_0.id
    # tile_4_0.next[TileConnectionType.down] = tile_4_1.id
    #
    # tile_4_1.next[TileConnectionType.left] = tile_3_1.id
    # tile_4_1.next[TileConnectionType.up] = tile_4_0.id
    # tile_4_1.next[TileConnectionType.down] = tile_4_2.id
    #
    # tile_4_2.next[TileConnectionType.left] = tile_3_2.id
    # tile_4_2.next[TileConnectionType.up] = tile_4_1.id
    # tile_4_2.next[TileConnectionType.down] = tile_4_3.id
    #
    # tile_4_3.next[TileConnectionType.left] = tile_3_3.id
    # tile_4_3.next[TileConnectionType.up] = tile_4_2.id
    # tile_4_3.next[TileConnectionType.down] = tile_4_4.id
    #
    # tile_4_4.next[TileConnectionType.left] = tile_3_4.id
    # tile_4_4.next[TileConnectionType.up] = tile_4_3.id
    #
    # ##############################################################################
    #
    # ######################### define a single 5x5 island #########################
    # localIsland: Island = Island(
    #     name="roshar",
    #     id=str(uuid.uuid4()),
    #     tiles={
    #         # row 0
    #         tile_0_0.id: tile_0_0,
    #         tile_0_1.id: tile_0_1,
    #         tile_0_2.id: tile_0_2,
    #         tile_0_3.id: tile_0_3,
    #         tile_0_4.id: tile_0_4,
    #
    #         # row 1
    #         tile_1_0.id: tile_1_0,
    #         tile_1_1.id: tile_1_1,
    #         tile_1_2.id: tile_1_2,
    #         tile_1_3.id: tile_1_3,
    #         tile_1_4.id: tile_1_4,
    #
    #         # row 2
    #         tile_2_0.id: tile_2_0,
    #         tile_2_1.id: tile_2_1,
    #         tile_2_2.id: tile_2_2,
    #         tile_2_3.id: tile_2_3,
    #         tile_2_4.id: tile_2_4,
    #
    #         # row 3
    #         tile_3_0.id: tile_3_0,
    #         tile_3_1.id: tile_3_1,
    #         tile_3_2.id: tile_3_2,
    #         tile_3_3.id: tile_3_3,
    #         tile_3_4.id: tile_3_4,
    #
    #         # row 4
    #         tile_4_0.id: tile_4_0,
    #         tile_4_1.id: tile_4_1,
    #         tile_4_2.id: tile_4_2,
    #         tile_4_3.id: tile_4_3,
    #         tile_4_4.id: tile_4_4,
    #     }
    # )
    #
    # # add generated island and return
    # localWorld.islands[localIsland.id] = localIsland
    # return localWorld
