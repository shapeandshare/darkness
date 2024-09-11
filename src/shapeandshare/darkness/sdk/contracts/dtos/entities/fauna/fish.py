import logging
from enum import Enum

from ......server.clients.dao import DaoClient
from ...tiles.address import Address
from .....common.utils import generate_random_float
from ....types.entity import EntityType
from ..entity import Entity

logger = logging.getLogger()


class EntityFish(Entity):
    address: Address
    daoclient: DaoClient
    class Meta(Enum):
        EGG = 0
        LARVA = 1
        ADULT = 2
        MATURE = 3

    entity_type: EntityType = EntityType.FISH

    max_amount: int = 16
    mutation_rate: float = 1

    async def quantum(self) -> None:
        """ """
        # TODO: ...
        # logger.info("Fish entity quantum")
        # if generate_random_float() <= self.mutation_rate:

        if EntityFish.Meta(self.state) == EntityFish.Meta.EGG:
            if generate_random_float() <= self.mutation_rate:
                self.state = EntityFish.Meta.LARVA.value
                await self.daoclient.patch(address=self.address, document={"state": self.state})
        elif EntityFish.Meta(self.state) == EntityFish.Meta.LARVA:
            if generate_random_float() <= self.mutation_rate:
                self.state = EntityFish.Meta.ADULT.value
                await self.daoclient.patch(address=self.address, document={"state": self.state})
        elif EntityFish.Meta(self.state) == EntityFish.Meta.ADULT:
            if generate_random_float() <= self.mutation_rate:
                self.state = EntityFish.Meta.MATURE.value
                await self.daoclient.patch(address=self.address, document={"state": self.state})
        elif EntityFish.Meta(self.state) == EntityFish.Meta.MATURE:
            if generate_random_float() <= self.mutation_rate:
                if self.amount < self.max_amount:
                    self.amount = self.amount + 1
                    await self.daoclient.patch(address=self.address, document={"amount": self.amount})
                self.state = EntityFish.Meta.EGG.value
                await self.daoclient.patch(address=self.address, document={"state": self.state})

