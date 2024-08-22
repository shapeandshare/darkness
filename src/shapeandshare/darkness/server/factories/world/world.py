import uuid

from pydantic import BaseModel

from ....client.dao import DaoClient
from ....sdk.contracts.dtos.sdk.wrapped_data import WrappedData
from ....sdk.contracts.dtos.tiles.address import Address
from ....sdk.contracts.dtos.tiles.world import World


class WorldFactory(BaseModel):
    daoclient: DaoClient

    class Config:
        arbitrary_types_allowed = True

    async def create(self, name: str | None = None) -> str:
        if name is None:
            name = "darkness"
        world: World = World(id=str(uuid.uuid4()), name=name)
        address_world: Address = Address.model_validate({"world_id": world.id})

        response: WrappedData[World] = await self.daoclient.document_post(address=address_world, document=world)
        return response.data.id
