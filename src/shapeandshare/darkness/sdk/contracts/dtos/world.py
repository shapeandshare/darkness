from pydantic import BaseModel


class World(BaseModel):
    id: str
    name: str
    rbac: dict = {}
    ids: set[str] = set()
