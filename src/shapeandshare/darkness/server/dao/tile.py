import logging
import os
import shutil
import uuid
from pathlib import Path

from ...sdk.contracts.dtos.sdk.wrapped_data import WrappedData
from ...sdk.contracts.dtos.tiles.tile import Tile
from ...sdk.contracts.errors.server.dao.conflict import DaoConflictError
from ...sdk.contracts.errors.server.dao.doesnotexist import DaoDoesNotExistError
from ...sdk.contracts.errors.server.dao.inconsistency import DaoInconsistencyError
from .abstract import AbstractDao

logger = logging.getLogger()


class TileDao(AbstractDao[Tile]):
    async def get(self, world_id: str, island_id: str, tile_id: str) -> WrappedData[Tile]:
        logger.debug("[TileDAO] getting tile data from storage")
        tile_metadata_path: Path = self._document_path(tokens={"world_id": world_id, "island_id": island_id, "tile_id": tile_id})
        if not tile_metadata_path.exists():
            raise DaoDoesNotExistError("tile metadata does not exist")
        with open(file=tile_metadata_path, mode="r", encoding="utf-8") as file:
            os.fsync(file)
            json_data: str = file.read()
        return WrappedData[Tile].model_validate_json(json_data)

    async def post(self, world_id: str, island_id: str, tile: Tile) -> WrappedData[Tile]:
        logger.debug("[TileDAO] posting tile data to storage")
        tile_metadata_path: Path = self._document_path(tokens={"world_id": world_id, "island_id": island_id, "tile_id": tile.id})
        if tile_metadata_path.exists():
            raise DaoConflictError("tile metadata already exists")
        if not tile_metadata_path.parents[2].exists():
            raise DaoDoesNotExistError("tile container (island) does not exist")
        if not tile_metadata_path.parent.exists():
            logger.debug("[TileDAO] tile metadata folder creating ..")
            tile_metadata_path.parent.mkdir(parents=True, exist_ok=True)
        nonce: str = str(uuid.uuid4())
        wrapped_data: WrappedData[Tile] = WrappedData[Tile](data=tile, nonce=nonce)
        wrapped_data_raw: str = wrapped_data.model_dump_json(exclude={"data": {"contents"}}, exclude_none=True)
        with open(file=tile_metadata_path, mode="w", encoding="utf-8") as file:
            file.write(wrapped_data_raw)
            os.fsync(file)

        # now validate we stored
        stored_tile: WrappedData[Tile] = await self.get(world_id=world_id, island_id=island_id, tile_id=tile.id)
        if stored_tile.nonce != nonce:
            msg: str = f"storage inconsistency detected while storing tile {tile.id} - nonce mismatch!"
            raise DaoInconsistencyError(msg)
        return stored_tile

    async def put(self, world_id: str, island_id: str, wrapped_tile: WrappedData[Tile]) -> WrappedData[Tile]:
        logger.debug("[TileDAO] putting tile data to storage")
        tile_metadata_path: Path = self._document_path(tokens={"world_id": world_id, "island_id": island_id, "tile_id": wrapped_tile.data.id})
        if not tile_metadata_path.parents[2].exists():
            raise DaoDoesNotExistError("tile container (island) does not exist")
        if not tile_metadata_path.parent.exists():
            logger.debug("[TileDAO] tile metadata folder creating ..")
            tile_metadata_path.parent.mkdir(parents=True, exist_ok=True)

        # see if we have a pre-existing nonce to verify against
        try:
            previous_state: WrappedData[Tile] = await self.get(world_id=world_id, island_id=island_id, tile_id=wrapped_tile.data.id)
            if previous_state.nonce != wrapped_tile.nonce:
                msg: str = f"storage inconsistency detected while putting tile {wrapped_tile.data.id} - nonce mismatch!"
                raise DaoInconsistencyError(msg)
        except DaoDoesNotExistError:
            # then no nonce to verify against.
            pass

        # if we made it this far we are safe to update

        nonce: str = str(uuid.uuid4())
        wrapped_data: WrappedData[Tile] = WrappedData[Tile](data=wrapped_tile.data, nonce=nonce)
        wrapped_data_raw: str = wrapped_data.model_dump_json(exclude={"data": {"contents"}}, exclude_none=True)
        with open(file=tile_metadata_path, mode="w", encoding="utf-8") as file:
            file.write(wrapped_data_raw)
            os.fsync(file)

        # now validate we stored
        stored_tile: WrappedData[Tile] = await self.get(world_id=world_id, island_id=island_id, tile_id=wrapped_data.data.id)
        if stored_tile.nonce != nonce:
            msg: str = f"storage inconsistency detected while verifying put tile {wrapped_data.data.id} - nonce mismatch!"
            raise DaoInconsistencyError(msg)
        return stored_tile

    async def patch(self, world_id: str, island_id: str, tile_id: str, tile: dict) -> WrappedData[Tile]:
        logger.debug("[TileDAO] patching tile data to storage")
        tile_metadata_path: Path = self._document_path(tokens={"world_id": world_id, "island_id": island_id, "tile_id": tile_id})
        if not tile_metadata_path.parents[2].exists():
            raise DaoDoesNotExistError("tile container (island) does not exist")
        if not tile_metadata_path.parent.exists():
            logger.debug("[TileDAO] tile metadata folder creating ..")
            tile_metadata_path.parent.mkdir(parents=True, exist_ok=True)

        previous_state: WrappedData[Tile] = await self.get(world_id=world_id, island_id=island_id, tile_id=tile_id)

        # if we made it this far we are safe to update

        # merge
        nonce: str = str(uuid.uuid4())
        previous_state_dict = previous_state.data.model_dump()
        new_state = TileDao.recursive_dict_merge(previous_state_dict, tile)
        wrapped_data: WrappedData[Tile] = WrappedData[Tile](data=new_state, nonce=nonce)

        # serialize to storage
        wrapped_data_raw: str = wrapped_data.model_dump_json(exclude_none=True)
        with open(file=tile_metadata_path, mode="w", encoding="utf-8") as file:
            file.write(wrapped_data_raw)
            os.fsync(file)

        # now validate we stored
        stored_entity: WrappedData[Tile] = await self.get(world_id=world_id, island_id=island_id, tile_id=wrapped_data.data.id)
        if stored_entity.nonce != nonce:
            msg: str = f"storage inconsistency detected while verifying patched tile {wrapped_data.data.id} - nonce mismatch!"
            raise DaoInconsistencyError(msg)
        return stored_entity

    async def delete(self, world_id: str, island_id: str, tile_id: str) -> bool:
        logger.debug("[TileDAO] deleting tile data from storage")
        tile_metadata_path: Path = self._document_path(tokens={"world_id": world_id, "island_id": island_id, "tile_id": tile_id})
        if not tile_metadata_path.exists():
            raise DaoDoesNotExistError("tile metadata does not exist")
        # remove "tile_id"/ and lower
        shutil.rmtree(tile_metadata_path.parent)
        return True
