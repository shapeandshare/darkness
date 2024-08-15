from enum import Enum


class EntityType(str, Enum):
    UNKNOWN = "unknown"

    GRASS = "grass"
    TREE = "tree"

    FISH = "fish"
