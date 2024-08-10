import logging
import shutil
import uuid
from pathlib import Path

from pydantic import BaseModel

from ...sdk.contracts.dtos.island_lite import IslandLite
from ...sdk.contracts.dtos.sdk.wrapped_data import WrappedData
from ...sdk.contracts.errors.server.dao.conflict import DaoConflictError
from ...sdk.contracts.errors.server.dao.doesnotexist import DaoDoesNotExistError
from ...sdk.contracts.errors.server.dao.inconsistency import DaoInconsistencyError
from ...sdk.contracts.types.tile import TileType

logger = logging.getLogger()


class IslandDao(BaseModel):
    # ["base"]  / "worlds" / "world_id" / "islands" / "island_id" / metadata.json
    storage_base_path: Path

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.storage_base_path.mkdir(parents=True, exist_ok=True)

    ### Internal ##################################

    def _island_metadata_path(self, world_id: str, island_id: str) -> Path:
        # ["base"] / "worlds" / "world_id" / "islands" / "island_id" / metadata.json
        return self.storage_base_path / "worlds" / world_id / "islands" / island_id / "metadata.json"

    def generate(self, world_id: str, name: str | None, dimensions: tuple[int, int], biome: TileType) -> str:
        logger.debug("[IslandService] generating island skeleton")
        if name is None:
            name = "roshar"
        island: IslandLite = IslandLite(id=str(uuid.uuid4()), name=name, dimensions=dimensions, biome=biome)
        self.post(world_id=world_id, island=island)
        return island.id

    def get(self, world_id: str, island_id: str) -> WrappedData[IslandLite]:
        logger.debug("[IslandService] getting island metadata from storage")
        island_metadata_path: Path = self._island_metadata_path(world_id=world_id, island_id=island_id)
        if not island_metadata_path.exists():
            raise DaoDoesNotExistError("island metadata does not exist")
        with open(file=island_metadata_path.resolve().as_posix(), mode="r", encoding="utf-8") as file:
            json_data: str = file.read()
        return WrappedData[IslandLite].model_validate_json(json_data)

    def post(self, world_id: str, island: IslandLite) -> None:
        logger.debug("[IslandService] posting island metadata to storage")
        island_metadata_path: Path = self._island_metadata_path(world_id=world_id, island_id=island.id)
        if island_metadata_path.exists():
            raise DaoConflictError("island metadata already exists")
        if not island_metadata_path.parent.exists():
            logger.debug("[IslandService] island metadata folder creating ..")
            island_metadata_path.parent.mkdir(parents=True, exist_ok=True)

        nonce: str = str(uuid.uuid4())
        wrapped_data: WrappedData[IslandLite] = WrappedData[IslandLite](data=island, nonce=nonce)
        wrapped_data_raw: str = wrapped_data.model_dump_json(indent=4)
        with open(file=island_metadata_path.resolve().as_posix(), mode="w", encoding="utf-8") as file:
            file.write(wrapped_data_raw)

        # now validate we stored
        stored_island: WrappedData[IslandLite] = self.get(world_id=world_id, island_id=island.id)
        if stored_island.nonce != nonce:
            msg: str = f"storage inconsistency detected while storing island {island.id} - nonce mismatch!"
            raise DaoInconsistencyError(msg)

    def put(self, world_id: str, island: IslandLite) -> None:
        logger.debug("[IslandService] putting island metadata to storage")
        island_metadata_path: Path = self._island_metadata_path(world_id=world_id, island_id=island.id)
        if not island_metadata_path.parent.exists():
            logger.debug("[IslandService] island metadata folder creating ..")
            island_metadata_path.parent.mkdir(parents=True, exist_ok=True)

        nonce: str = str(uuid.uuid4())
        wrapped_data: WrappedData[IslandLite] = WrappedData[IslandLite](data=island, nonce=nonce)
        wrapped_data_raw: str = wrapped_data.model_dump_json(indent=4)
        with open(file=island_metadata_path.resolve().as_posix(), mode="w", encoding="utf-8") as file:
            file.write(wrapped_data_raw)

        # now validate we stored
        stored_island: WrappedData[IslandLite] = self.get(world_id=world_id, island_id=island.id)
        if stored_island.nonce != nonce:
            msg: str = f"storage inconsistency detected while storing island {island.id} - nonce mismatch!"
            raise DaoInconsistencyError(msg)

    def put_safe(self, world_id: str, wrapped_island: WrappedData[IslandLite]) -> None:
        logger.debug("[IslandService] putting island data to storage")
        island_metadata_path: Path = self._island_metadata_path(world_id=world_id, island_id=wrapped_island.data.id)
        if not island_metadata_path.parent.exists():
            logger.debug("[IslandService] island metadata folder creating ..")
            island_metadata_path.parent.mkdir(parents=True, exist_ok=True)

        # see if we have a pre-existing nonce to verify against
        try:
            previous_state = self.get(world_id=world_id, island_id=wrapped_island.data.id)
            if previous_state.nonce != wrapped_island.nonce:
                msg: str = (
                    f"storage inconsistency detected while putting island {wrapped_island.data.id} - nonce mismatch!"
                )
                raise DaoInconsistencyError(msg)
        except DaoDoesNotExistError:
            # then no nonce to verify against.
            pass

        # if we made it this far we are safe to update

        nonce: str = str(uuid.uuid4())
        wrapped_data: WrappedData[IslandLite] = WrappedData[IslandLite](data=wrapped_island.data, nonce=nonce)
        wrapped_data_raw: str = wrapped_data.model_dump_json(indent=4)
        with open(file=island_metadata_path.resolve().as_posix(), mode="w", encoding="utf-8") as file:
            file.write(wrapped_data_raw)

        # now validate we stored
        stored_island: WrappedData[IslandLite] = self.get(world_id=world_id, island_id=wrapped_data.data.id)
        if stored_island.nonce != nonce:
            msg: str = (
                f"storage inconsistency detected while verifying put island {wrapped_data.data.id} - nonce mismatch!"
            )
            raise DaoInconsistencyError(msg)

    def delete(self, world_id: str, island_id: str) -> None:
        logger.debug("[IslandService] deleting island data from storage")
        island_metadata_path: Path = self._island_metadata_path(world_id=world_id, island_id=island_id)
        if not island_metadata_path.exists():
            raise DaoDoesNotExistError("island metadata does not exist")
        # remove "island_id"/ and lower
        shutil.rmtree(island_metadata_path.parent.resolve().as_posix())
