from ...contracts.dtos.island import Island
from ...contracts.types.tile import TileType
from .flat import FlatIslandFactory
from .flatland import FlatLandFactory


class IslandFactory(FlatIslandFactory):
    @staticmethod
    def flat(dim: tuple[int, int], biome: TileType) -> Island:
        return FlatIslandFactory.flat(universal_dim=dim, biome=biome)

    @staticmethod
    def flatland(dim: tuple[int, int], biome: TileType) -> Island:
        return FlatLandFactory.generate(universal_dim=dim, biome=biome)
