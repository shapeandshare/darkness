from .entity import EntityRequest


class EntityPatchRequest(EntityRequest):
    partial: dict
