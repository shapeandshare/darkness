import uuid

from pydantic import BaseModel

from ....sdk.contracts.dtos.sdk.wrapped_data import WrappedData
from ....sdk.contracts.dtos.tiles.address import Address
from ....sdk.contracts.dtos.tiles.world import World
from ...services.dao import DaoService


class WorldFactory(BaseModel):
    daoservice: DaoService

    async def create(self, name: str | None = None) -> str:
        if name is None:
            name = "darkness"
        world: World = World(id=str(uuid.uuid4()), name=name)
        address_world: Address = Address.model_validate({"world_id": world.id})
        response: WrappedData[World] = await self.daoservice.post(address=address_world, document=world)
        return response.data.id
