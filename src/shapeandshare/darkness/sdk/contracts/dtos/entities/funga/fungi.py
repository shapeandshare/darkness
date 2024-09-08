import logging
from enum import Enum

from ....types.entity import EntityType
from ..entity import Entity

logger = logging.getLogger()


class EntityFungi(Entity):
    entity_type: EntityType = EntityType.FUNGI

    async def quantum(self) -> None:
        """ """
        # logger.info("fungi entity quantum")

    class Meta(Enum):
        SPORE = 0
        MYCELIUM = 1
        FRUIT = 2
        MATURE = 3
