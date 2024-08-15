import logging
import os
import uuid
from pathlib import Path

from pydantic import BaseModel

from ...sdk.contracts.dtos.sdk.wrapped_data import WrappedData
from ...sdk.contracts.dtos.tiles.tile import Tile
from ...sdk.contracts.errors.server.dao.conflict import DaoConflictError
from ...sdk.contracts.errors.server.dao.doesnotexist import DaoDoesNotExistError
from ...sdk.contracts.errors.server.dao.inconsistency import DaoInconsistencyError

logger = logging.getLogger()


class TileDao(BaseModel):
    # ["base"] / "worlds" / "wold_id" / "islands" / "island_id" / "tiles" / "tile_id" / "metadata.json"
    storage_base_path: Path

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.storage_base_path.mkdir(parents=True, exist_ok=True)

    ### Internal ##################################

    def _tile_path(self, world_id: str, island_id: str, tile_id: str) -> Path:
        # ["base"] / "worlds" / "wold_id" / "islands" / "island_id" / "tiles" / "tile_id.json"
        return self.storage_base_path / "worlds" / world_id / "islands" / island_id / "tiles" / tile_id / "metadata.json"

    async def get(self, world_id: str, island_id: str, tile_id: str) -> WrappedData[Tile]:
        logger.debug("[TileDAO] getting tile data from storage")
        tile_metadata_path: Path = self._tile_path(world_id=world_id, island_id=island_id, tile_id=tile_id)
        if not tile_metadata_path.exists():
            raise DaoDoesNotExistError("tile metadata does not exist")
        with open(file=tile_metadata_path, mode="r", encoding="utf-8") as file:
            os.fsync(file)
            json_data: str = file.read()
        return WrappedData[Tile].model_validate_json(json_data)

    async def post(self, world_id: str, island_id: str, tile: Tile) -> None:
        logger.debug("[TileDAO] posting tile data to storage")
        tile_metadata_path: Path = self._tile_path(world_id=world_id, island_id=island_id, tile_id=tile.id)
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

    async def put_safe(self, world_id: str, island_id: str, wrapped_tile: WrappedData[Tile]) -> None:
        logger.debug("[TileDAO] putting tile data to storage")
        tile_metadata_path: Path = self._tile_path(world_id=world_id, island_id=island_id, tile_id=wrapped_tile.data.id)
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

    async def delete(self, world_id: str, island_id: str, tile_id: str) -> None:
        logger.debug("[TileDAO] deleting tile data from storage")
        tile_metadata_path: Path = self._tile_path(world_id=world_id, island_id=island_id, tile_id=tile_id)
        if not tile_metadata_path.exists():
            raise DaoDoesNotExistError("tile metadata does not exist")
        os.remove(path=tile_metadata_path)
