import logging
from enum import Enum

from ....types.entity import EntityType
from ..entity import Entity

logger = logging.getLogger()


class EntityTree(Entity):
    entity_type: EntityType = EntityType.TREE

    async def quantum(self) -> None:
        """ """
        # logger.info("tree entity quantum")

    class Meta(Enum):
        SEED = 0
        SAPLING = 1
        FRUIT = 2
        MATURE = 3
