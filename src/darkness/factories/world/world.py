import uuid
from ..island.island import IslandFactory
from ...contracts.dtos.island import Island
from ...contracts.dtos.world import World
from ...contracts.types.tile import TileType


class WorldFactory:
    @staticmethod
    def generate() -> World:
        # 1. blank, named world
        return World(
            id=str(uuid.uuid4()),
            name="darkness",
        )

    @staticmethod
    def island_discover(target_world: World, dim: tuple[int, int], biome: TileType) -> str:
        local_island: Island = IslandFactory.generate(dim=dim, biome=biome)
        target_world.islands[local_island.id] = local_island
        return local_island.id
