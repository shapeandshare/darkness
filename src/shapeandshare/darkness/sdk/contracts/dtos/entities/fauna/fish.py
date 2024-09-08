import logging
from enum import Enum

from .....common.utils import generate_random_float
from ....types.entity import EntityType
from ..entity import Entity

logger = logging.getLogger()


class EntityFish(Entity):
    entity_type: EntityType = EntityType.FISH

    mutation_rate: float = 0.1

    async def quantum(self) -> None:
        """ """
        # TODO: ...
        # logger.info("Fish entity quantum")
        if generate_random_float() <= self.mutation_rate:
            pass

    class Meta(Enum):
        EGG = 0
        LARVA = 1
        ADULT = 2
        MATURE = 3
