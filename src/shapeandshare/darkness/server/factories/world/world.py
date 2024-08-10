import uuid

from pydantic import BaseModel

from ....sdk.contracts.dtos.world_lite import WorldLite
from ...dao.world import WorldDao


class WorldFactory(BaseModel):
    worlddao: WorldDao

    def create(self, name: str | None = None) -> str:
        if name is None:
            name = "darkness"
        world: WorldLite = WorldLite(id=str(uuid.uuid4()), name=name)
        self.worlddao.post(world=world)
        return world.id
