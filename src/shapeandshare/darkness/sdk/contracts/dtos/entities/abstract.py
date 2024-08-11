import time

from pydantic import BaseModel

from ...types.entity import EntityType


class AbstractEntity(BaseModel):
    id: str
    name: str | None = None
    rbac: dict = {}
    entity_type: EntityType = EntityType.UNKNOWN
    updated: float | None = None  # unix timestamp

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # set creation time as last time updated
        self.updated = time.time()
