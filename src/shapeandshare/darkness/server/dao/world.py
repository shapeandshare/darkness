import logging

from ...sdk.contracts.dtos.sdk.wrapped_data import WrappedData
from ...sdk.contracts.dtos.tiles.world import World
from .abstract import AbstractDao

logger = logging.getLogger()


class WorldDao(AbstractDao[World]):
    async def post(self, tokens: dict, document: World) -> WrappedData[World]:
        logger.debug("[WorldDAO] posting world metadata to storage")
        tokens["world_id"] = document.id
        return await self.post_partial(tokens=tokens, document=document, exclude={"data": {"next", "contents"}})

    async def put(self, tokens: dict, wrapped_document: WrappedData[World]) -> WrappedData[World]:
        logger.debug("[WorldDAO] putting world data to storage")
        world_id: str = wrapped_document.data.id
        tokens["world_id"] = world_id
        return await self.put_partial(tokens=tokens, wrapped_document=wrapped_document, exclude={"data": {"next", "contents"}})

    async def patch(self, tokens: dict, document: dict) -> WrappedData[World]:
        if "id" in document:
            tokens["world_id"] = document["id"]
        return await self.patch_partial(tokens=tokens, document=document, exclude={"data": {"next", "contents"}})
