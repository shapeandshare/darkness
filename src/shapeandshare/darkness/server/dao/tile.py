import logging
import os
import uuid
from pathlib import Path

from ...sdk.contracts.dtos.sdk.wrapped_data import WrappedData
from ...sdk.contracts.dtos.tiles.tile import Tile
from ...sdk.contracts.errors.server.dao.doesnotexist import DaoDoesNotExistError
from ...sdk.contracts.errors.server.dao.inconsistency import DaoInconsistencyError
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

        logger.debug("[TileDAO] patching tile data to storage")
        tile_metadata_path: Path = self._document_path(tokens=tokens)
        if not tile_metadata_path.parents[2].exists():
            raise DaoDoesNotExistError("tile container (island) does not exist")
        if not tile_metadata_path.parent.exists():
            logger.debug("[TileDAO] tile metadata folder creating ..")
            tile_metadata_path.parent.mkdir(parents=True, exist_ok=True)

        previous_state: WrappedData[Tile] = await self.get(tokens=tokens)
        previous_state.data = Tile.model_validate(previous_state.data)
        # if we made it this far we are safe to update

        # merge
        nonce: str = str(uuid.uuid4())
        previous_state_dict = previous_state.data.model_dump()
        new_state = TileDao.recursive_dict_merge(previous_state_dict, document)
        wrapped_data: WrappedData[Tile] = WrappedData[Tile](data=new_state, nonce=nonce)

        # serialize to storage
        wrapped_data_raw: str = wrapped_data.model_dump_json(exclude_none=True)
        with open(file=tile_metadata_path, mode="w", encoding="utf-8") as file:
            file.write(wrapped_data_raw)
            os.fsync(file)

        # now validate we stored
        stored_entity: WrappedData[Tile] = await self.get(tokens=tokens)
        stored_entity.data = Tile.model_validate(stored_entity.data)
        if stored_entity.nonce != nonce:
            msg: str = f"storage inconsistency detected while verifying patched tile {wrapped_data.data.id} - nonce mismatch!"
            raise DaoInconsistencyError(msg)
        return stored_entity
