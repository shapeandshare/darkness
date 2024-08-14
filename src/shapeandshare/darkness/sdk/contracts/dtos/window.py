from pydantic import BaseModel

from src.shapeandshare.darkness.server.dao.tile import TileDao

from ..types.connection import TileConnectionType
from .coordinate import Coordinate
from .sdk.wrapped_data import WrappedData
from .tiles.island import Island
from .tiles.tile import Tile


class Window(BaseModel):
    # 2D window
    min: Coordinate
    max: Coordinate

    # async def get_tile_ids(self):
    #     origin_id = self.island.origin_id
    #
    #     range_x_min: int = self.min.x - 1
    #     range_x_max: int = self.max.x
    #     range_y_min: int = self.min.x - 1
    #     range_y_max: int = self.max.y
    #
    #     # 1. origin -> 1_1 and get id of 1_1
    #
    #     # def get_node_right_of(node_id=origin_id, length=range_x_min)
    #     async def get_node_to_the(node_id: str, length: int, con: TileConnectionType) -> str:
    #         if length == 0:
    #             return node_id
    #         else:
    #             tile: WrappedData[Tile] = await self.tiledao.get(world_id=self.world_id, island_id=self.island.id, tile_id=node_id)
    #             next_id: str = tile.data.next[con]
    #             return await get_node_to_the(node_id=next_id, length=length-1, con=con)
    #
    #     # 1 -> x
    #     x_ref = await get_node_to_the(node_id=self.island.origin, length=range_x_min, con=TileConnectionType.RIGHT)
    #     # x -> y
    #     y_ref = await get_node_to_the(node_id=x_ref, length=range_y_min, con=TileConnectionType.DOWN)
    #     # y_ref is now 1,1 of the tile window
    #
    #     # 2. build connected graph
    #     ids: list[str] = []
    #     ids.append(y_ref)
    #
    #     for x in range(range_x_min, range_x_max):
    #         local_x = x + 1
    #         local_x_ref = await get_node_to_the(node_id=y_ref, length=1, con=TileConnectionType.RIGHT)
    #         for y in range(range_y_min, range_y_max):
    #             local_y = y + 1
    #             local_y_ref = await get_node_to_the(node_id=local_x_ref, length=1, con=TileConnectionType.DOWN)
    #             ids.append(local_y_ref)
    #
