from pydantic import BaseModel


class WorldLite(BaseModel):
    id: str
    name: str
    rbac: dict = {}
    island_ids: set[str] = set()
