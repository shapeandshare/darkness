import logging
import os
import shutil
import uuid
from copy import deepcopy
from pathlib import Path

from pydantic import BaseModel

from ...sdk.contracts.dtos.sdk.wrapped_data import WrappedData
from ...sdk.contracts.dtos.world import World
from ...sdk.contracts.errors.server.dao.conflict import DaoConflictError
from ...sdk.contracts.errors.server.dao.doesnotexist import DaoDoesNotExistError
from ...sdk.contracts.errors.server.dao.inconsistency import DaoInconsistencyError

logger = logging.getLogger()


class WorldDao(BaseModel):
    # ["base"]  / "worlds" / "world_id" / metadata.json
    storage_base_path: Path

    def _world_metadata_path(self, world_id: str) -> Path:
        # ["base"] / "worlds" / "world_id" / metadata.json
        return self.storage_base_path / "worlds" / world_id / "metadata.json"

    ### Internal ##################################

    async def get(self, world_id: str) -> WrappedData[World]:
        logger.debug("[WorldDAO] getting world metadata from storage")
        world_metadata_path: Path = self._world_metadata_path(world_id=world_id)
        if not world_metadata_path.exists():
            raise DaoDoesNotExistError("world metadata does not exist")
        with open(file=world_metadata_path.resolve().as_posix(), mode="r", encoding="utf-8") as file:
            os.fsync(file)
            json_data: str = file.read()
        return WrappedData[World].model_validate_json(json_data)

    async def post(self, world: World) -> None:
        local_world = deepcopy(world)
        logger.debug("[WorldDAO] posting world metadata to storage")
        world_metadata_path: Path = self._world_metadata_path(world_id=local_world.id)
        if world_metadata_path.exists():
            raise DaoConflictError("world metadata already exists")
        if not world_metadata_path.parent.exists():
            logger.debug("[WorldDAO] world metadata folder creating ..")
            world_metadata_path.parent.mkdir(parents=True, exist_ok=True)

        nonce: str = str(uuid.uuid4())
        wrapped_data: WrappedData[World] = WrappedData[World](data=local_world, nonce=nonce)
        wrapped_data_raw: str = wrapped_data.model_dump_json(exclude={"data": {"next", "contents"}})
        with open(file=world_metadata_path.resolve().as_posix(), mode="w", encoding="utf-8") as file:
            file.write(wrapped_data_raw)
            os.fsync(file)

        # now validate we stored
        stored_world: WrappedData[World] = await self.get(world_id=local_world.id)
        if stored_world.nonce != nonce:
            msg: str = f"storage inconsistency detected while storing world {local_world.id} - nonce mismatch!"
            raise DaoInconsistencyError(msg)

    async def put_safe(self, wrapped_world: WrappedData[World]) -> None:
        local_wrapped_world = deepcopy(wrapped_world)
        world_id: str = local_wrapped_world.data.id

        logger.debug("[WorldDAO] putting world data to storage")
        world_metadata_path: Path = self._world_metadata_path(world_id=world_id)
        if not world_metadata_path.parent.exists():
            logger.debug("[WorldDAO] world metadata folder creating ..")
            world_metadata_path.parent.mkdir(parents=True, exist_ok=True)

        # see if we have a pre-existing nonce to verify against
        try:
            previous_state: WrappedData[World] = await self.get(world_id=world_id)
            if previous_state.nonce != local_wrapped_world.nonce:
                msg: str = f"storage inconsistency detected while putting world {world_id} - nonce mismatch!"
                raise DaoInconsistencyError(msg)
        except DaoDoesNotExistError:
            # then no nonce to verify against.
            pass

        # if we made it this far we are safe to update

        nonce: str = str(uuid.uuid4())
        wrapped_data: WrappedData[World] = WrappedData[World](data=local_wrapped_world.data, nonce=nonce)
        wrapped_data_raw: str = wrapped_data.model_dump_json(exclude={"data": {"next", "contents"}})
        with open(file=world_metadata_path.resolve().as_posix(), mode="w", encoding="utf-8") as file:
            file.write(wrapped_data_raw)
            os.fsync(file)

        # now validate we stored
        stored_world: WrappedData[World] = await self.get(world_id=world_id)
        if stored_world.nonce != nonce:
            msg: str = (
                f"storage inconsistency detected while verifying put world {wrapped_data.data.id} - nonce mismatch!"
            )
            raise DaoInconsistencyError(msg)

    async def delete(self, world_id: str) -> None:
        logger.debug("[WorldDAO] deleting world data from storage")
        world_metadata_path: Path = self._world_metadata_path(world_id=world_id)
        if not world_metadata_path.exists():
            raise DaoDoesNotExistError("world metadata does not exist")
        # remove "world_id"/ and lower
        shutil.rmtree(world_metadata_path.parent.resolve().as_posix())
