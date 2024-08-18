from enum import Enum


class EntityType(str, Enum):
    UNKNOWN = "unknown"

    GRASS = "grass"
    TREE = "tree"
    FRUIT = "fruit"

    FISH = "fish"

    MYCELIUM = "mycelium"
    MUSHROOM = "mushroom"
