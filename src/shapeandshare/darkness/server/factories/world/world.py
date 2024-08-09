import uuid

from pydantic import BaseModel

# from ....sdk.contracts.dtos.island import Island
# from ....sdk.contracts.dtos.world import World
from ....sdk.contracts.dtos.world_lite import WorldLite

# from ....sdk.contracts.types.tile import TileType
from ...dao.world import WorldDao

# from ..island.abstract import IslandFactory


class WorldFactory(BaseModel):
    worlddao: WorldDao

    def create(self, name: str | None = None) -> str:
        if name is None:
            name = "darkness"
        world: WorldLite = WorldLite(id=str(uuid.uuid4()), name=name)
        self.worlddao.post(world=world)
        return world.id

    # @staticmethod
    # def generate(name: str | None = None) -> World:
    #     if name is None:
    #         name = "darkness"
    #
    #     # 1. blank, named world
    #     return World(
    #         id=str(uuid.uuid4()),
    #         name=name,
    #     )

    # @staticmethod
    # def island_discover(target_world: World, dimensions: tuple[int, int], biome: TileType) -> str:
    #     local_island: Island = IslandFactory.basic(dimensions=dimensions, biome=biome)
    #     target_world.islands[local_island.id] = local_island
    #     return local_island.id
