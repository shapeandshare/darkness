import uuid

from pydantic import BaseModel

from ....sdk.contracts.dtos.tiles.address import Address
from ....sdk.contracts.dtos.tiles.world import World
from ...clients.dao import DaoClient


class WorldFactory(BaseModel):
    daoclient: DaoClient

    class Config:
        arbitrary_types_allowed = True

    async def create(self, name: str | None = None) -> str:
        if name is None:
            name = "darkness"
        world: World = World(id=str(uuid.uuid4()), name=name)
        address_world: Address = Address.model_validate({"world_id": world.id})

        await self.daoclient.post(address=address_world, document=world)
        return world.id
