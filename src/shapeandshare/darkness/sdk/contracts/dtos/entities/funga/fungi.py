import logging
from enum import Enum

from ......sdk.contracts.dtos.tiles.address import Address
from ......server.clients.dao import DaoClient
from .....common.utils import generate_random_float
from ....types.entity import EntityType
from ..entity import Entity

logger = logging.getLogger()


class EntityFungi(Entity):
    address: Address
    daoclient: DaoClient

    class Meta(Enum):
        SPORE = 0
        MYCELIUM = 1
        FRUIT = 2
        MATURE = 3

    entity_type: EntityType = EntityType.FUNGI

    max_amount: int = 16
    mutation_rate: float = 0.01

    async def quantum(self) -> None:
        """ """
        # logger.info("fungi entity quantum")

        if EntityFungi.Meta(self.state) == EntityFungi.Meta.SPORE:
            if generate_random_float() <= self.mutation_rate:
                self.state = EntityFungi.Meta.MYCELIUM.value
                await self.daoclient.patch(address=self.address, document={"state": self.state})
        elif EntityFungi.Meta(self.state) == EntityFungi.Meta.MYCELIUM:
            if generate_random_float() <= self.mutation_rate:
                self.state = EntityFungi.Meta.FRUIT.value
                await self.daoclient.patch(address=self.address, document={"state": self.state})
        elif EntityFungi.Meta(self.state) == EntityFungi.Meta.FRUIT:
            if generate_random_float() <= self.mutation_rate:
                self.state = EntityFungi.Meta.MATURE.value
                await self.daoclient.patch(address=self.address, document={"state": self.state})
        elif EntityFungi.Meta(self.state) == EntityFungi.Meta.MATURE:
            if generate_random_float() <= self.mutation_rate:
                if self.amount < self.max_amount:
                    self.amount = self.amount + 1
                    await self.daoclient.patch(address=self.address, document={"amount": self.amount})
                self.state = EntityFungi.Meta.SPORE.value
                await self.daoclient.patch(address=self.address, document={"state": self.state})
