import time

from pydantic import BaseModel

from ..types.entity import EntityType


class Entity(BaseModel):
    id: str
    entity_type: EntityType
    updated: float | None = None  # unix timestamp
    rbac: dict = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # set creation time as last time updated
        self.updated = time.time()
