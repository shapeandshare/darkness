from pydantic import BaseModel

from .island import Island


class World(BaseModel):
    id: str
    name: str
    rbac: dict = {}
    islands: dict[str, Island] = {}
