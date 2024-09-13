import logging
from enum import Enum

from ......server.clients.dao import DaoClient
from .....common.utils import generate_random_float
from ....types.entity import EntityType
from ...tiles.address import Address
from ..entity import Entity

logger = logging.getLogger()


class EntityGrass(Entity):
    address: Address
    daoclient: DaoClient

    class Meta(Enum):
        SEED = 0
        BLADE = 1
        FRUIT = 2
        MATURE = 3

    entity_type: EntityType = EntityType.GRASS

    max_amount: int = 16
    mutation_rate: float = 0.01

    async def quantum(self) -> None:
        """ """
        if EntityGrass.Meta(self.state) == EntityGrass.Meta.SEED:
            if generate_random_float() <= self.mutation_rate:
                self.state = EntityGrass.Meta.BLADE.value
                await self.daoclient.patch(address=self.address, document={"state": self.state})
        elif EntityGrass.Meta(self.state) == EntityGrass.Meta.BLADE:
            if generate_random_float() <= self.mutation_rate:
                self.state = EntityGrass.Meta.FRUIT.value
                await self.daoclient.patch(address=self.address, document={"state": self.state})
        elif EntityGrass.Meta(self.state) == EntityGrass.Meta.FRUIT:
            if generate_random_float() <= self.mutation_rate:
                self.state = EntityGrass.Meta.MATURE.value
                await self.daoclient.patch(address=self.address, document={"state": self.state})
        elif EntityGrass.Meta(self.state) == EntityGrass.Meta.MATURE:
            if generate_random_float() <= self.mutation_rate:
                if self.amount < self.max_amount:
                    self.amount = self.amount + 1
                    await self.daoclient.patch(address=self.address, document={"amount": self.amount})
                self.state = EntityGrass.Meta.SEED.value
                await self.daoclient.patch(address=self.address, document={"state": self.state})
