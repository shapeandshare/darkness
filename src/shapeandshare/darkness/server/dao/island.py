import logging
from copy import deepcopy

from ...sdk.contracts.dtos.sdk.wrapped_data import WrappedData
from ...sdk.contracts.dtos.tiles.island import Island
from .abstract import AbstractDao

logger = logging.getLogger()


class IslandDao(AbstractDao[Island]):
    async def post(self, tokens: dict, document: Island) -> WrappedData[Island]:
        tokens_copy = deepcopy(tokens)
        tokens_copy["island_id"] = document.id
        return await self.post_partial(tokens=tokens_copy, document=document, exclude={"data": {"next", "contents"}})

    async def put(self, tokens: dict, wrapped_document: WrappedData[Island]) -> WrappedData[Island]:
        tokens_copy = deepcopy(tokens)
        tokens_copy["island_id"] = wrapped_document.data.id
        return await self.put_partial(
            tokens=tokens_copy, wrapped_document=wrapped_document, exclude={"data": {"next", "contents"}}
        )

    async def patch(self, tokens: dict, document: dict) -> WrappedData[Island]:
        document_copy = deepcopy(document)
        if "id" in document_copy:
            del document_copy["id"]
        return await self.patch_partial(tokens=tokens, document=document_copy, exclude={"data": {"next", "contents"}})
