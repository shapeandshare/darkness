import uuid

from pydantic import BaseModel

from ....sdk.contracts.dtos.tiles.world import World
from ...dao.world import WorldDao


class WorldFactory(BaseModel):
    worlddao: WorldDao

    async def create(self, name: str | None = None) -> str:
        if name is None:
            name = "darkness"
        world: World = World(id=str(uuid.uuid4()), name=name)
        await self.worlddao.post(world=world)
        return world.id
