from enum import Enum


class DaoDocumentType(str, Enum):
    WORLD = "world"
    CHUNK = "chunk"
    TILE = "tile"
    ENTITY = "entity"
