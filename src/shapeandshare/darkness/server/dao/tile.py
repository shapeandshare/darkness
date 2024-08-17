import logging

from ...sdk.contracts.dtos.sdk.wrapped_data import WrappedData
from ...sdk.contracts.dtos.tiles.tile import Tile
from .abstract import AbstractDao

logger = logging.getLogger()


class TileDao(AbstractDao[Tile]):
    async def post(self, tokens: dict, document: Tile) -> WrappedData[Tile]:
        tokens["tile_id"] = document.id
        return await self.post_partial(tokens=tokens, document=document, exclude={"data": {"contents"}})

    async def put(self, tokens: dict, wrapped_document: WrappedData[Tile]) -> WrappedData[Tile]:
        tokens["tile_id"] = wrapped_document.data.id
        return await self.put_partial(tokens=tokens, wrapped_document=wrapped_document, exclude={"data": {"contents"}})

    async def patch(self, tokens: dict, document: dict) -> WrappedData[Tile]:
        if "id" in document:
            del document["id"]
        return await self.patch_partial(tokens=tokens, document=document, exclude={"data": {"contents"}})
