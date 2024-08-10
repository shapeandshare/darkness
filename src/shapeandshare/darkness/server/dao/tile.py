import logging
import os
import uuid
from pathlib import Path

from pydantic import BaseModel

from ...sdk.contracts.dtos.sdk.wrapped_data import WrappedData
from ...sdk.contracts.dtos.tile import Tile
from ...sdk.contracts.errors.server.dao.conflict import DaoConflictError
from ...sdk.contracts.errors.server.dao.doesnotexist import DaoDoesNotExistError
from ...sdk.contracts.errors.server.dao.inconsistency import DaoInconsistencyError
from ...sdk.contracts.types.tile import TileType

logger = logging.getLogger()


class TileDao(BaseModel):
    # ["base"] / "worlds" / "wold_id" / "islands" / "island_id" / "tiles" / "tile_id.json"
    storage_base_path: Path

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.storage_base_path.mkdir(parents=True, exist_ok=True)

    ### Internal ##################################

    def _tile_path(self, world_id: str, island_id: str, tile_id: str) -> Path:
        # ["base"] / "worlds" / "wold_id" / "islands" / "island_id" / "tiles" / "tile_id.json"
        return self.storage_base_path / "worlds" / world_id / "islands" / island_id / "tiles" / f"{tile_id}.json"

    def generate(self, world_id: str, island_id: str, tile_type: TileType = TileType.UNKNOWN) -> str:
        logger.debug("[TileService] generating tile skeleton")
        tile: Tile = Tile(id=str(uuid.uuid4()), tile_type=tile_type)
        self.post(world_id=world_id, island_id=island_id, tile=tile)
        return tile.id

    def get(self, world_id: str, island_id: str, tile_id: str) -> WrappedData[Tile]:
        logger.debug("[TileService] getting island data from storage")
        tile_metadata_path: Path = self._tile_path(world_id=world_id, island_id=island_id, tile_id=tile_id)
        if not tile_metadata_path.exists():
            raise DaoDoesNotExistError("tile metadata does not exist")
        with open(file=tile_metadata_path.resolve().as_posix(), mode="r", encoding="utf-8") as file:
            json_data: str = file.read()
        return WrappedData[Tile].model_validate_json(json_data)

    def post(self, world_id: str, island_id: str, tile: Tile) -> None:
        logger.debug("[TileService] posting tile data to storage")
        tile_metadata_path: Path = self._tile_path(world_id=world_id, island_id=island_id, tile_id=tile.id)
        if tile_metadata_path.exists():
            raise DaoConflictError("tile metadata already exists")
        if not tile_metadata_path.parent.exists():
            logger.debug("[TileService] tile metadata folder creating ..")
            tile_metadata_path.parent.mkdir(parents=True, exist_ok=True)
        nonce: str = str(uuid.uuid4())
        wrapped_data: WrappedData[Tile] = WrappedData[Tile](data=tile, nonce=nonce)
        wrapped_data_raw: str = wrapped_data.model_dump_json(indent=4)
        with open(file=tile_metadata_path.resolve().as_posix(), mode="w", encoding="utf-8") as file:
            file.write(wrapped_data_raw)

        # now validate we stored
        stored_tile: WrappedData[Tile] = self.get(world_id=world_id, island_id=island_id, tile_id=tile.id)
        if stored_tile.nonce != nonce:
            msg: str = f"storage inconsistency detected while storing tile {tile.id} - nonce mismatch!"
            raise DaoInconsistencyError(msg)

    def put(self, world_id: str, island_id: str, tile: Tile) -> None:
        logger.debug("[TileService] putting tile data to storage")
        tile_metadata_path: Path = self._tile_path(world_id=world_id, island_id=island_id, tile_id=tile.id)
        if not tile_metadata_path.parent.exists():
            logger.debug("[TileService] tile metadata folder creating ..")
            tile_metadata_path.parent.mkdir(parents=True, exist_ok=True)
        nonce: str = str(uuid.uuid4())
        wrapped_data: WrappedData[Tile] = WrappedData[Tile](data=tile, nonce=nonce)
        wrapped_data_raw: str = wrapped_data.model_dump_json(indent=4)
        with open(file=tile_metadata_path.resolve().as_posix(), mode="w", encoding="utf-8") as file:
            file.write(wrapped_data_raw)

        # now validate we stored
        stored_tile: WrappedData[Tile] = self.get(world_id=world_id, island_id=island_id, tile_id=tile.id)
        if stored_tile.nonce != nonce:
            msg: str = f"storage inconsistency detected while storing tile {tile.id} - nonce mismatch!"
            raise DaoInconsistencyError(msg)

    def put_safe(self, world_id: str, island_id: str, wrapped_tile: WrappedData[Tile]) -> None:
        logger.debug("[TileService] putting tile data to storage")
        tile_metadata_path: Path = self._tile_path(world_id=world_id, island_id=island_id, tile_id=wrapped_tile.data.id)
        if not tile_metadata_path.parent.exists():
            logger.debug("[TileService] tile metadata folder creating ..")
            tile_metadata_path.parent.mkdir(parents=True, exist_ok=True)

        # see if we have a pre-existing nonce to verify against
        try:
            previous_state = self.get(world_id=world_id, island_id=island_id, tile_id=wrapped_tile.data.id)
            if previous_state.nonce != wrapped_tile.nonce:
                msg: str = f"storage inconsistency detected while putting tile {wrapped_tile.data.id} - nonce mismatch!"
                raise DaoInconsistencyError(msg)
        except DaoDoesNotExistError:
            # then no nonce to verify against.
            pass

        # if we made it this far we are safe to update

        nonce: str = str(uuid.uuid4())
        wrapped_data: WrappedData[Tile] = WrappedData[Tile](data=wrapped_tile.data, nonce=nonce)
        wrapped_data_raw: str = wrapped_data.model_dump_json(indent=4)
        with open(file=tile_metadata_path.resolve().as_posix(), mode="w", encoding="utf-8") as file:
            file.write(wrapped_data_raw)

        # now validate we stored
        stored_tile: WrappedData[Tile] = self.get(world_id=world_id, island_id=island_id, tile_id=wrapped_data.data.id)
        if stored_tile.nonce != nonce:
            msg: str = (
                f"storage inconsistency detected while verifying put tile {wrapped_data.data.id} - nonce mismatch!"
            )
            raise DaoInconsistencyError(msg)

    def delete(self, world_id: str, island_id: str, tile_id: str) -> None:
        logger.debug("[TileService] deleting tile data from storage")
        tile_metadata_path: Path = self._tile_path(world_id=world_id, island_id=island_id, tile_id=tile_id)
        if not tile_metadata_path.exists():
            raise DaoDoesNotExistError("tile metadata does not exist")
        os.remove(path=tile_metadata_path.resolve().as_posix())
