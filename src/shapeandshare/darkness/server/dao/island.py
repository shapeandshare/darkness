import logging

from ...sdk.contracts.dtos.sdk.wrapped_data import WrappedData
from ...sdk.contracts.dtos.tiles.island import Island
from .abstract import AbstractDao

logger = logging.getLogger()


class IslandDao(AbstractDao[Island]):
    async def post(self, tokens: dict, document: Island) -> WrappedData[Island]:
        tokens["island_id"] = document.id
        return await self.post_partial(tokens=tokens, document=document, exclude={"data": {"next", "contents"}})

    async def put(self, tokens: dict, wrapped_document: WrappedData[Island]) -> WrappedData[Island]:
        tokens["island_id"] = wrapped_document.data.id
        return await self.put_partial(tokens=tokens, wrapped_document=wrapped_document, exclude={"data": {"next", "contents"}})

    async def patch(self, tokens: dict, document: dict) -> WrappedData[Island]:
        if "id" in document:
            del document["id"]
        return await self.patch_partial(tokens=tokens, document=document, exclude={"data": {"next", "contents"}})
