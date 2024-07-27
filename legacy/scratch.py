# from ..dtos.contracts.world import World
#
#
# # import uuid
# #
# # from darkness.dtos.contracts.island import Island
# # from darkness.dtos.contracts.tile import Tile
# # from darkness.dtos.contracts.types.connection import TileConnectionType
# # from darkness.dtos.contracts.types.tile import TileType
# # from darkness.dtos.contracts.world import World
# #
# # ### build tiles #######################################################################################
# # # tile_x_y | (0,0) top left -- (x,y) -- bottom right
# #
# # ### column 0 ###########################################
# # tile_0_0: Tile = Tile(id="tile_0_0", tileType=TileType.water)
# # tile_0_1: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.water)
# # tile_0_2: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.water)
# # tile_0_3: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.water)
# # tile_0_4: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.water)
# #
# # ### column 1 ###########################################
# # tile_1_0: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.water)
# # tile_1_1: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.shore)
# # tile_1_2: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.shore)
# # tile_1_3: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.shore)
# # tile_1_4: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.water)
# #
# # ### column 2 ###########################################
# # tile_2_0: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.water)
# # tile_2_1: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.shore)
# # tile_2_2: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.dirt)
# # tile_2_3: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.shore)
# # tile_2_4: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.water)
# #
# # ### column 3 ###########################################
# # tile_3_0: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.water)
# # tile_3_1: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.shore)
# # tile_3_2: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.shore)
# # tile_3_3: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.shore)
# # tile_3_4: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.water)
# #
# # ### column 4 ###########################################
# # tile_4_0: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.water)
# # tile_4_1: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.water)
# # tile_4_2: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.water)
# # tile_4_3: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.water)
# # tile_4_4: Tile = Tile(id=str(uuid.uuid4()), tileType=TileType.water)
# #
# #
# #
# # ### connect tiles #######################################################################################
# #
# #
# # ### column 0 ##############################################################################
# #
# # tile_0_0.next[TileConnectionType.right] = tile_1_0.id
# # tile_0_0.next[TileConnectionType.down] = tile_0_1.id
# #
# # tile_0_1.next[TileConnectionType.up] =  tile_0_0.id
# # tile_0_1.next[TileConnectionType.right] = tile_1_1.id
# # tile_0_1.next[TileConnectionType.down] = tile_0_2.id
# #
# # tile_0_2.next[TileConnectionType.up] = tile_0_1.id
# # tile_0_2.next[TileConnectionType.right] = tile_1_2.id
# # tile_0_2.next[TileConnectionType.down] = tile_0_3.id
# #
# # tile_0_3.next[TileConnectionType.up] = tile_0_2.id
# # tile_0_3.next[TileConnectionType.right] = tile_1_3.id
# # tile_0_3.next[TileConnectionType.down] = tile_0_4.id
# #
# # tile_0_4.next[TileConnectionType.up] = tile_0_3.id
# # tile_0_4.next[TileConnectionType.right] = tile_1_4.id
# #
# # ### column 1 ##############################################################################
# #
# # tile_1_0.next[TileConnectionType.left] = tile_0_0.id
# # tile_1_0.next[TileConnectionType.right] = tile_2_0.id
# # tile_1_0.next[TileConnectionType.down] = tile_1_1.id
# #
# # tile_1_1.next[TileConnectionType.left] = tile_0_1.id
# # tile_1_1.next[TileConnectionType.right] = tile_2_1.id
# # tile_1_1.next[TileConnectionType.up] = tile_1_0.id
# # tile_1_1.next[TileConnectionType.down] = tile_1_2.id
# #
# # tile_1_2.next[TileConnectionType.left] = tile_0_2.id
# # tile_1_2.next[TileConnectionType.right] = tile_2_2.id
# # tile_1_2.next[TileConnectionType.up] = tile_1_1.id
# # tile_1_2.next[TileConnectionType.down] = tile_1_3.id
# #
# # tile_1_3.next[TileConnectionType.left] = tile_0_3.id
# # tile_1_3.next[TileConnectionType.right] = tile_2_3.id
# # tile_1_3.next[TileConnectionType.up] =  tile_1_2.id
# # tile_1_3.next[TileConnectionType.down] = tile_1_4.id
# #
# # tile_1_4.next[TileConnectionType.left] = tile_0_4.id
# # tile_1_4.next[TileConnectionType.right] = tile_2_4.id
# # tile_1_4.next[TileConnectionType.up] = tile_1_3.id
# #
# # ### column 2 ##############################################################################
# #
# # tile_2_0.next[TileConnectionType.left] = tile_1_0.id
# # tile_2_0.next[TileConnectionType.right] = tile_3_0.id
# # tile_2_0.next[TileConnectionType.down] = tile_2_1.id
# #
# # tile_2_1.next[TileConnectionType.left] = tile_1_1.id
# # tile_2_1.next[TileConnectionType.right] = tile_3_1.id
# # tile_2_1.next[TileConnectionType.up] = tile_2_0.id
# # tile_2_1.next[TileConnectionType.down] = tile_2_2.id
# #
# # tile_2_2.next[TileConnectionType.left] = tile_1_2.id
# # tile_2_2.next[TileConnectionType.right] = tile_3_2.id
# # tile_2_2.next[TileConnectionType.up] = tile_2_1.id
# # tile_2_2.next[TileConnectionType.down] = tile_2_3.id
# #
# # tile_2_3.next[TileConnectionType.left] = tile_1_3.id
# # tile_2_3.next[TileConnectionType.right] = tile_3_3.id
# # tile_2_3.next[TileConnectionType.up] = tile_2_2.id
# # tile_2_3.next[TileConnectionType.down] = tile_2_4.id
# #
# # tile_2_4.next[TileConnectionType.left] = tile_1_4.id
# # tile_2_4.next[TileConnectionType.right] = tile_3_4.id
# # tile_2_4.next[TileConnectionType.up] = tile_2_3.id
# #
# # ### column 3 ##############################################################################
# #
# # tile_3_0.next[TileConnectionType.left] = tile_2_0.id
# # tile_3_0.next[TileConnectionType.right] = tile_4_0.id
# # tile_3_0.next[TileConnectionType.down] = tile_3_1.id
# #
# # tile_3_1.next[TileConnectionType.left] = tile_2_1.id
# # tile_3_1.next[TileConnectionType.right] = tile_4_1.id
# # tile_3_1.next[TileConnectionType.up] = tile_3_0.id
# # tile_3_1.next[TileConnectionType.down] = tile_3_2.id
# #
# # tile_3_2.next[TileConnectionType.left] = tile_2_2.id
# # tile_3_2.next[TileConnectionType.right] = tile_4_2.id
# # tile_3_2.next[TileConnectionType.up] = tile_3_1.id
# # tile_3_2.next[TileConnectionType.down] = tile_3_3.id
# #
# # tile_3_3.next[TileConnectionType.left] = tile_2_3.id
# # tile_3_3.next[TileConnectionType.right] = tile_4_3.id
# # tile_3_3.next[TileConnectionType.up] = tile_3_2.id
# # tile_3_3.next[TileConnectionType.down] = tile_3_4.id
# #
# # tile_3_4.next[TileConnectionType.left] = tile_2_4.id
# # tile_3_4.next[TileConnectionType.right] = tile_4_4.id
# # tile_3_4.next[TileConnectionType.up] = tile_3_3.id
# #
# # ### column 4 ##############################################################################
# #
# # tile_4_0.next[TileConnectionType.left] = tile_3_0.id
# # tile_4_0.next[TileConnectionType.down] = tile_4_1.id
# #
# # tile_4_1.next[TileConnectionType.left] = tile_3_1.id
# # tile_4_1.next[TileConnectionType.up] = tile_4_0.id
# # tile_4_1.next[TileConnectionType.down] = tile_4_2.id
# #
# # tile_4_2.next[TileConnectionType.left] = tile_3_2.id
# # tile_4_2.next[TileConnectionType.up] = tile_4_1.id
# # tile_4_2.next[TileConnectionType.down] = tile_4_3.id
# #
# # tile_4_3.next[TileConnectionType.left] = tile_3_3.id
# # tile_4_3.next[TileConnectionType.up] = tile_4_2.id
# # tile_4_3.next[TileConnectionType.down] = tile_4_4.id
# #
# # tile_4_4.next[TileConnectionType.left] = tile_3_4.id
# # tile_4_4.next[TileConnectionType.up] = tile_4_3.id
# #
# #
# #
# # ##############################################################################
# #
# #
# # ######################### define a single 5x5 island #########################
# # localIsland: Island = Island(
# #     name="roshar",
# #     id=str(uuid.uuid4()),
# #     tiles={
# #         # row 0
# #         tile_0_0.id: tile_0_0,
# #         tile_0_1.id: tile_0_1,
# #         tile_0_2.id: tile_0_2,
# #         tile_0_3.id: tile_0_3,
# #         tile_0_4.id: tile_0_4,
# #
# #         # row 1
# #         tile_1_0.id: tile_1_0,
# #         tile_1_1.id: tile_1_1,
# #         tile_1_2.id: tile_1_2,
# #         tile_1_3.id: tile_1_3,
# #         tile_1_4.id: tile_1_4,
# #
# #         # row 2
# #         tile_2_0.id: tile_2_0,
# #         tile_2_1.id: tile_2_1,
# #         tile_2_2.id: tile_2_2,
# #         tile_2_3.id: tile_2_3,
# #         tile_2_4.id: tile_2_4,
# #
# #         # row 3
# #         tile_3_0.id: tile_3_0,
# #         tile_3_1.id: tile_3_1,
# #         tile_3_2.id: tile_3_2,
# #         tile_3_3.id: tile_3_3,
# #         tile_3_4.id: tile_3_4,
# #
# #         # row 4
# #         tile_4_0.id: tile_4_0,
# #         tile_4_1.id: tile_4_1,
# #         tile_4_2.id: tile_4_2,
# #         tile_4_3.id: tile_4_3,
# #         tile_4_4.id: tile_4_4,
# #     }
# # )
# #
# # localWorld: World = World(
# #     id=str(uuid.uuid4()),
# #     name="darkness",
# #     islands={
# #         # A Single island `darkness`
# #         localIsland.id: localIsland
# #     }
# # )
# #
# #
# #
# # print(localWorld.model_dump_json(indent=4))
#
#
# if __name__ == "__main__":
#     localWorld: World = defaultWorld(universal_dim=(5, 5))
#     print(localWorld.model_dump_json(indent=4))
