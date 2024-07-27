from ..contracts.dtos.island import Island
from ..contracts.types.biome import BiomeType
from src.darkness.factories.world.flat import FlatWorldFactory
from src.darkness.factories.world.world import WorldFactory


class IslandService:
    def get(self, id: str) -> Island | None:
        return FlatWorldFactory.generate(universal_dim=(5,5)).islands[id]

    def generate(self, dim: tuple[int, int], terrian: BiomeType):
        return WorldFactory.generate(dim=dim, terrian=terrian)
