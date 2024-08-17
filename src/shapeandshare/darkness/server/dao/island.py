import logging
import os
import shutil
import uuid
from pathlib import Path

from ...sdk.contracts.dtos.sdk.wrapped_data import WrappedData
from ...sdk.contracts.dtos.tiles.island import Island
from ...sdk.contracts.errors.server.dao.conflict import DaoConflictError
from ...sdk.contracts.errors.server.dao.doesnotexist import DaoDoesNotExistError
from ...sdk.contracts.errors.server.dao.inconsistency import DaoInconsistencyError
from .abstract import AbstractDao

logger = logging.getLogger()


class IslandDao(AbstractDao[Island]):
    async def get(self, tokens: dict) -> WrappedData[Island]:
        logger.debug("[IslandDAO] getting island metadata from storage")
        island_metadata_path: Path = self._document_path(tokens=tokens)
        if not island_metadata_path.exists():
            raise DaoDoesNotExistError("island metadata does not exist")
        with open(file=island_metadata_path, mode="r", encoding="utf-8") as file:
            os.fsync(file)
            json_data: str = file.read()
        return WrappedData[Island].model_validate_json(json_data)

    async def post(self, tokens: dict, island: Island) -> WrappedData[Island]:
        logger.debug("[IslandDAO] posting island metadata to storage")
        tokens["island_id"] = island.id

        island_metadata_path: Path = self._document_path(tokens=tokens)
        if island_metadata_path.exists():
            raise DaoConflictError("island metadata already exists")
        if not island_metadata_path.parents[2].exists():
            raise DaoDoesNotExistError("island container (world) does not exist")
        if not island_metadata_path.parent.exists():
            logger.debug("[IslandDAO] island metadata folder creating ..")
            island_metadata_path.parent.mkdir(parents=True, exist_ok=True)

        nonce: str = str(uuid.uuid4())
        wrapped_data: WrappedData[Island] = WrappedData[Island](data=island, nonce=nonce)
        wrapped_data_raw: str = wrapped_data.model_dump_json(exclude={"data": {"next", "contents"}})
        with open(file=island_metadata_path, mode="w", encoding="utf-8") as file:
            file.write(wrapped_data_raw)
            os.fsync(file)

        # now validate we stored
        stored_island: WrappedData[Island] = await self.get(tokens=tokens)
        if stored_island.nonce != nonce:
            msg: str = f"storage inconsistency detected while storing island {island.id} - nonce mismatch!"
            raise DaoInconsistencyError(msg)
        return stored_island

    async def put(self, tokens: dict, wrapped_island: WrappedData[Island]) -> WrappedData[Island]:
        logger.debug("[IslandDAO] putting island data to storage")
        tokens["island_id"] = wrapped_island.data.id
        island_metadata_path: Path = self._document_path(tokens=tokens)
        if not island_metadata_path.parents[2].exists():
            raise DaoDoesNotExistError("island container (world) does not exist")
        if not island_metadata_path.parent.exists():
            logger.debug("[IslandDAO] island metadata folder creating ..")
            island_metadata_path.parent.mkdir(parents=True, exist_ok=True)

        # see if we have a pre-existing nonce to verify against
        try:
            previous_state = await self.get(tokens=tokens)
            if previous_state.nonce != wrapped_island.nonce:
                msg: str = f"storage inconsistency detected while putting island {wrapped_island.data.id} - nonce mismatch!"
                raise DaoInconsistencyError(msg)
        except DaoDoesNotExistError:
            # then no nonce to verify against.
            pass

        # if we made it this far we are safe to update

        nonce: str = str(uuid.uuid4())
        wrapped_data: WrappedData[Island] = WrappedData[Island](data=wrapped_island.data, nonce=nonce)
        wrapped_data_raw: str = wrapped_data.model_dump_json(exclude={"data": {"next", "contents"}})
        with open(file=island_metadata_path, mode="w", encoding="utf-8") as file:
            file.write(wrapped_data_raw)
            os.fsync(file)

        # now validate we stored
        stored_island: WrappedData[Island] = await self.get(tokens=tokens)
        if stored_island.nonce != nonce:
            msg: str = f"storage inconsistency detected while verifying put island {wrapped_data.data.id} - nonce mismatch!"
            raise DaoInconsistencyError(msg)
        return stored_island

    async def patch(self, tokens: dict, island: dict) -> WrappedData[Island]:
        logger.debug("[IslandDAO] patching tile data to storage")
        if "id" in island:
            tokens["island_id"] = island["id"]
        island_metadata_path: Path = self._document_path(tokens=tokens)
        if not island_metadata_path.parents[2].exists():
            raise DaoDoesNotExistError("island container (world) does not exist")
        if not island_metadata_path.parent.exists():
            logger.debug("[IslandDAO] island metadata folder creating ..")
            island_metadata_path.parent.mkdir(parents=True, exist_ok=True)

        previous_state: WrappedData[Island] = await self.get(tokens=tokens)

        # if we made it this far we are safe to update

        # merge
        nonce: str = str(uuid.uuid4())
        previous_state_dict = previous_state.data.model_dump()
        new_state = IslandDao.recursive_dict_merge(previous_state_dict, island)
        wrapped_data: WrappedData[Island] = WrappedData[Island](data=new_state, nonce=nonce)

        # serialize to storage
        wrapped_data_raw: str = wrapped_data.model_dump_json(exclude_none=True)
        with open(file=island_metadata_path, mode="w", encoding="utf-8") as file:
            file.write(wrapped_data_raw)
            os.fsync(file)

        # now validate we stored
        stored_entity: WrappedData[Island] = await self.get(tokens=tokens)
        if stored_entity.nonce != nonce:
            msg: str = f"storage inconsistency detected while verifying patched island {wrapped_data.data.id} - nonce mismatch!"
            raise DaoInconsistencyError(msg)
        return stored_entity

    async def delete(self, tokens: dict) -> bool:
        logger.debug("[IslandDAO] deleting island data from storage")
        island_metadata_path: Path = self._document_path(tokens=tokens)
        if not island_metadata_path.exists():
            raise DaoDoesNotExistError("island metadata does not exist")
        # remove "island_id"/ and lower
        shutil.rmtree(island_metadata_path.parent)
        return True
