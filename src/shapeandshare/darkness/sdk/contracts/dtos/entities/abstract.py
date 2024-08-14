from pydantic import BaseModel

from ...types.entity import EntityType


class AbstractEntity(BaseModel):
    id: str
    name: str | None = None
    rbac: dict = {}
    entity_type: EntityType = EntityType.UNKNOWN

    # future ..
    amount: float = 0
    state: int = 0
