import logging
import os
import uuid
from pathlib import Path

from pydantic import BaseModel

from ...sdk.contracts.dtos.sdk.wrapped_data import WrappedData
from ...sdk.contracts.dtos.tile import Tile
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
            raise Exception("[TileService] tile metadata does not exist - 404, not found, put or patch instead?")
        with open(file=tile_metadata_path.resolve().as_posix(), mode="r", encoding="utf-8") as file:
            json_data: str = file.read()
        return WrappedData[Tile].model_validate_json(json_data)

    def post(self, world_id: str, island_id: str, tile: Tile) -> None:
        logger.debug("[TileService] posting tile data to storage")
        tile_metadata_path: Path = self._tile_path(world_id=world_id, island_id=island_id, tile_id=tile.id)
        if tile_metadata_path.exists():
            raise Exception("[TileService] tile metadata already exists - 403, conflict, put or patch instead?")
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
            raise Exception(
                f"[TileService] Storage inconsistency detected while storing tile {tile.id} - nonce mismatch!"
            )

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
            raise Exception(
                f"[TileService] Storage inconsistency detected while storing tile {tile.id} - nonce mismatch!"
            )

    def delete(self, world_id: str, island_id: str, tile_id: str) -> None:
        logger.debug("[TileService] deleting tile data from storage")
        tile_metadata_path: Path = self._tile_path(world_id=world_id, island_id=island_id, tile_id=tile_id)
        if not tile_metadata_path.exists():
            raise Exception("[TileService] tile metadata does not exist - 404, not found")
        os.remove(path=tile_metadata_path.resolve().as_posix())
