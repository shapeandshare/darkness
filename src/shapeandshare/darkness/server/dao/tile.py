import logging

from ...sdk.contracts.dtos.sdk.wrapped_data import WrappedData
from ...sdk.contracts.dtos.tiles.tile import Tile
from .abstract import AbstractDao

logger = logging.getLogger()


class TileDao(AbstractDao[Tile]):
    async def post(self, tokens: dict, document: Tile) -> WrappedData[Tile]:
        logger.debug("[TileDAO] posting tile data to storage")
        # add tile_id to tokens
        tokens["tile_id"] = document.id
        return await self.post_partial(tokens=tokens, document=document, exclude={"data": {"contents"}})

    async def put(self, tokens: dict, wrapped_document: WrappedData[Tile]) -> WrappedData[Tile]:
        tokens["tile_id"] = wrapped_document.data.id
        logger.debug("[TileDAO] putting tile data to storage")
        return await self.put_partial(tokens=tokens, wrapped_document=wrapped_document, exclude={"data": {"contents"}})

    async def patch(self, tokens: dict, document: dict) -> WrappedData[Tile]:
        if "id" in document:
            tokens["tile_id"] = document["id"]
        return await self.patch_partial(tokens=tokens, document=document, exclude={"data": {"contents"}})
