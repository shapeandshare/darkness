from .entity import EntityRequest


class EntityDeleteRequest(EntityRequest):
    parent: bool
