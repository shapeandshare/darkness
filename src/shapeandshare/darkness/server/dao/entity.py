import logging
from copy import deepcopy

from ...sdk.contracts.dtos.entities.entity import Entity
from ...sdk.contracts.dtos.sdk.wrapped_data import WrappedData
from .abstract import AbstractDao

logger = logging.getLogger()


class EntityDao(AbstractDao[Entity]):
    async def post(self, tokens: dict, document: Entity) -> WrappedData[Entity]:
        tokens_copy = deepcopy(tokens)
        tokens_copy["entity_id"] = document.id
        return await self.post_partial(tokens=tokens_copy, document=document)

    async def put(self, tokens: dict, wrapped_document: WrappedData[Entity]) -> WrappedData[Entity]:
        tokens_copy = deepcopy(tokens)
        tokens_copy["tile_id"] = wrapped_document.data.id
        return await self.put_partial(tokens=tokens_copy, wrapped_document=wrapped_document)

    async def patch(self, tokens: dict, document: dict) -> WrappedData[Entity]:
        document_copy = deepcopy(document)
        if "id" in document_copy:
            del document_copy["id"]
        return await self.patch_partial(tokens=tokens, document=document_copy)
