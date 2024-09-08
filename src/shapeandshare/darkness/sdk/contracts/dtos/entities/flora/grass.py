import logging
from enum import Enum

from ....types.entity import EntityType
from ..entity import Entity

logger = logging.getLogger()


class EntityGrass(Entity):
    entity_type: EntityType = EntityType.GRASS

    async def quantum(self) -> None:
        """ """
        # logger.info("Grass entity quantum")

    class Meta(Enum):
        SEED = 0
        BLADE = 1
        FRUIT = 2
        MATURE = 3
