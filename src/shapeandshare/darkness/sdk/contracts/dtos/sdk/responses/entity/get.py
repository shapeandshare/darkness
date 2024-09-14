from pydantic import BaseModel

from ....entities.entity import Entity


class EntityGetResponse(BaseModel):
    entity: Entity
