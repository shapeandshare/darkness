import logging

from ...sdk.contracts.dtos.entities.entity import Entity
from ...sdk.contracts.dtos.sdk.wrapped_data import WrappedData
from .abstract import AbstractDao

logger = logging.getLogger()


class EntityDao(AbstractDao[Entity]):
    async def post(self, tokens: dict, document: Entity) -> WrappedData[Entity]:
        logger.debug("[EntityDAO] posting entity data to storage")
        tokens["entity_id"] = document.id
        return await self.post_partial(tokens=tokens, document=document)

    async def put(self, tokens: dict, wrapped_document: WrappedData[Entity]) -> WrappedData[Entity]:
        logger.debug("[EntityDAO] putting entity data to storage")
        tokens["tile_id"] = wrapped_document.data.id
        return await self.put_partial(tokens=tokens, wrapped_document=wrapped_document)

    async def patch(self, tokens: dict, document: dict) -> WrappedData[Entity]:
        if "id" in document:
            tokens["entity_id"] = document["id"]
        return await self.patch_partial(tokens=tokens, document=document)
