from enum import Enum


class ChunkQuantumType(str, Enum):
    ALL = "all"
    TILE = "tile"
    ENTITY = "entity"
