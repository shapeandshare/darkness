from pydantic import BaseModel

from .....dtos.island import Island


class IslandGetResponse(BaseModel):
    island: Island
