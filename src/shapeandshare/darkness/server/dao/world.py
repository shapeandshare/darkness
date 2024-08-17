import logging
import os
import shutil
import uuid
from pathlib import Path

from ...sdk.contracts.dtos.sdk.wrapped_data import WrappedData
from ...sdk.contracts.dtos.tiles.world import World
from ...sdk.contracts.errors.server.dao.conflict import DaoConflictError
from ...sdk.contracts.errors.server.dao.doesnotexist import DaoDoesNotExistError
from ...sdk.contracts.errors.server.dao.inconsistency import DaoInconsistencyError
from .abstract import AbstractDao

logger = logging.getLogger()


class WorldDao(AbstractDao[World]):
    async def post(self, world: World) -> WrappedData[World]:
        logger.debug("[WorldDAO] posting world metadata to storage")
        world_metadata_path: Path = self._document_path(tokens={"world_id": world.id})
        if world_metadata_path.exists():
            raise DaoConflictError("world metadata already exists")
        if not world_metadata_path.parent.exists():
            logger.debug("[WorldDAO] world metadata folder creating ..")
            world_metadata_path.parent.mkdir(parents=True, exist_ok=True)

        nonce: str = str(uuid.uuid4())
        wrapped_data: WrappedData[World] = WrappedData[World](data=world, nonce=nonce)
        wrapped_data_raw: str = wrapped_data.model_dump_json(exclude={"data": {"next", "contents"}})
        with open(file=world_metadata_path, mode="w", encoding="utf-8") as file:
            file.write(wrapped_data_raw)
            os.fsync(file)

        # now validate we stored
        stored_world: WrappedData[World] = await self.get(tokens={"world_id": world.id})
        stored_world.data = World.model_validate(stored_world.data)
        if stored_world.nonce != nonce:
            msg: str = f"storage inconsistency detected while storing world {world.id} - nonce mismatch!"
            raise DaoInconsistencyError(msg)
        return stored_world

    async def put(self, wrapped_world: WrappedData[World]) -> WrappedData[World]:
        world_id: str = wrapped_world.data.id

        logger.debug("[WorldDAO] putting world data to storage")
        world_metadata_path: Path = self._document_path(tokens={"world_id": world_id})
        if not world_metadata_path.parent.exists():
            logger.debug("[WorldDAO] world metadata folder creating ..")
            world_metadata_path.parent.mkdir(parents=True, exist_ok=True)

        # see if we have a pre-existing nonce to verify against
        try:
            previous_state: WrappedData[World] = await self.get(tokens={"world_id": world_id})
            previous_state.data = World.model_validate(previous_state.data)
            if previous_state.nonce != wrapped_world.nonce:
                msg: str = f"storage inconsistency detected while putting world {world_id} - nonce mismatch!"
                raise DaoInconsistencyError(msg)
        except DaoDoesNotExistError:
            # then no nonce to verify against.
            pass

        # if we made it this far we are safe to update

        nonce: str = str(uuid.uuid4())
        wrapped_data: WrappedData[World] = WrappedData[World](data=wrapped_world.data, nonce=nonce)
        wrapped_data_raw: str = wrapped_data.model_dump_json(exclude={"data": {"next", "contents"}})
        with open(file=world_metadata_path, mode="w", encoding="utf-8") as file:
            file.write(wrapped_data_raw)
            os.fsync(file)

        # now validate we stored
        stored_world: WrappedData[World] = await self.get(tokens={"world_id": world_id})
        stored_world.data = World.model_validate(stored_world.data)
        if stored_world.nonce != nonce:
            msg: str = f"storage inconsistency detected while verifying put world {wrapped_data.data.id} - nonce mismatch!"
            raise DaoInconsistencyError(msg)
        return stored_world

    async def patch(self, world_id: str, world: dict) -> WrappedData[World]:
        logger.debug("[WorldDAO] patching world data to storage")
        world_metadata_path: Path = self._document_path(tokens={"world_id": world_id})
        if not world_metadata_path.parents[2].exists():
            raise DaoDoesNotExistError("world container (universe) does not exist")
        if not world_metadata_path.parent.exists():
            logger.debug("[WorldDAO] world metadata folder creating ..")
            world_metadata_path.parent.mkdir(parents=True, exist_ok=True)

        previous_state: WrappedData[World] = await self.get(tokens={"world_id": world_id})
        previous_state.data = World.model_validate(previous_state.data)

        # if we made it this far we are safe to update

        # merge
        nonce: str = str(uuid.uuid4())
        previous_state_dict = previous_state.data.model_dump()
        new_state = WorldDao.recursive_dict_merge(previous_state_dict, world)
        wrapped_data: WrappedData[World] = WrappedData[World](data=new_state, nonce=nonce)

        # serialize to storage
        wrapped_data_raw: str = wrapped_data.model_dump_json(exclude_none=True)
        with open(file=world_metadata_path, mode="w", encoding="utf-8") as file:
            file.write(wrapped_data_raw)
            os.fsync(file)

        # now validate we stored
        stored_entity: WrappedData[World] = await self.get(tokens={"world_id": world_id})
        stored_entity.data = World.model_validate(stored_entity.data)
        if stored_entity.nonce != nonce:
            msg: str = f"storage inconsistency detected while verifying patched world {wrapped_data.data.id} - nonce mismatch!"
            raise DaoInconsistencyError(msg)
        return stored_entity

    async def delete(self, world_id: str) -> bool:
        logger.debug("[WorldDAO] deleting world data from storage")
        world_metadata_path: Path = self._document_path(tokens={"world_id": world_id})
        if not world_metadata_path.exists():
            raise DaoDoesNotExistError("world metadata does not exist")
        # remove "world_id"/ and lower
        shutil.rmtree(world_metadata_path.parent)
        return True
