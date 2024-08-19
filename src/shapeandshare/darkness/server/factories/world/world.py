import uuid

from pydantic import BaseModel

from ....sdk.contracts.dtos.tiles.world import World
from ...dao.dao import AbstractDao


class WorldFactory(BaseModel):
    worlddao: AbstractDao[World]

    async def create(self, name: str | None = None) -> str:
        if name is None:
            name = "darkness"
        world: World = World(id=str(uuid.uuid4()), name=name)
        tokens_world: dict = {"world_id": world.id}
        await self.worlddao.post(tokens=tokens_world, document=world)
        return world.id
