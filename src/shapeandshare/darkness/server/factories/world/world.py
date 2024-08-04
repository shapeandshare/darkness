import uuid

from ....sdk.contracts.dtos.island import Island
from ....sdk.contracts.dtos.world import World
from ....sdk.contracts.types.tile import TileType
from ..island.island import IslandFactory


class WorldFactory:
    @staticmethod
    def generate() -> World:
        # 1. blank, named world
        return World(
            id=str(uuid.uuid4()),
            name="darkness",
        )

    @staticmethod
    def island_discover(target_world: World, dimensions: tuple[int, int], biome: TileType) -> str:
        local_island: Island = IslandFactory.basic(dimensions=dimensions, biome=biome)
        target_world.islands[local_island.id] = local_island
        return local_island.id
