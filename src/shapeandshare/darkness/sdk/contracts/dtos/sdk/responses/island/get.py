from pydantic import BaseModel

from .....dtos.island_full import IslandFull
from ....island import Island


class IslandGetResponse(BaseModel):
    island: IslandFull | Island
