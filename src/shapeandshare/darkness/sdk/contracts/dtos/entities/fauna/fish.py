import logging
from enum import Enum

from ....types.entity import EntityType
from ..entity import Entity

logger = logging.getLogger()


class EntityFish(Entity):
    entity_type: EntityType = EntityType.FISH

    async def quantum(self) -> None:
        """ """
        # logger.info("Fish entity quantum")

    class Meta(Enum):
        EGG = 0
        LARVA = 1
        ADULT = 2
        MATURE = 3
