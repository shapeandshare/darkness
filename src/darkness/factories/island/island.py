from .flat import FlatIslandFactory
from ...contracts.dtos.island import Island
from ...contracts.types.tile import TileType


class IslandFactory(FlatIslandFactory):
    @staticmethod
    def generate(dim: tuple[int, int], biome: TileType) -> Island:
        return FlatIslandFactory.flat(universal_dim=dim, biome=biome)
