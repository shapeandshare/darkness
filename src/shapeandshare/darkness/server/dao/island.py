import logging
import os
import shutil
import uuid
from pathlib import Path

from ...sdk.contracts.dtos.sdk.wrapped_data import WrappedData
from ...sdk.contracts.dtos.tiles.island import Island
from ...sdk.contracts.errors.server.dao.doesnotexist import DaoDoesNotExistError
from ...sdk.contracts.errors.server.dao.inconsistency import DaoInconsistencyError
from .abstract import AbstractDao

logger = logging.getLogger()


class IslandDao(AbstractDao[Island]):
    async def post(self, tokens: dict, document: Island) -> WrappedData[Island]:
        logger.debug("[IslandDAO] posting island metadata to storage")
        tokens["island_id"] = document.id
        return await self.post_partial(tokens=tokens, document=document, exclude={"data": {"next", "contents"}})

    async def put(self, tokens: dict, wrapped_document: WrappedData[Island]) -> WrappedData[Island]:
        logger.debug("[IslandDAO] putting island data to storage")
        tokens["island_id"] = wrapped_document.data.id
        island_metadata_path: Path = self._document_path(tokens=tokens)
        if not island_metadata_path.parents[2].exists():
            raise DaoDoesNotExistError("island container (world) does not exist")
        if not island_metadata_path.parent.exists():
            logger.debug("[IslandDAO] island metadata folder creating ..")
            island_metadata_path.parent.mkdir(parents=True, exist_ok=True)

        # see if we have a pre-existing nonce to verify against
        try:
            previous_state = await self.get(tokens=tokens)
            previous_state.data = Island.model_validate(previous_state.data)
            if previous_state.nonce != wrapped_document.nonce:
                msg: str = f"storage inconsistency detected while putting island {wrapped_document.data.id} - nonce mismatch!"
                raise DaoInconsistencyError(msg)
        except DaoDoesNotExistError:
            # then no nonce to verify against.
            pass

        # if we made it this far we are safe to update

        nonce: str = str(uuid.uuid4())
        wrapped_data: WrappedData[Island] = WrappedData[Island](data=wrapped_document.data, nonce=nonce)
        wrapped_data_raw: str = wrapped_data.model_dump_json(exclude={"data": {"next", "contents"}})
        with open(file=island_metadata_path, mode="w", encoding="utf-8") as file:
            file.write(wrapped_data_raw)
            os.fsync(file)

        # now validate we stored
        stored_island: WrappedData[Island] = await self.get(tokens=tokens)
        stored_island.data = Island.model_validate(stored_island.data)
        if stored_island.nonce != nonce:
            msg: str = f"storage inconsistency detected while verifying put island {wrapped_data.data.id} - nonce mismatch!"
            raise DaoInconsistencyError(msg)
        return stored_island

    async def patch(self, tokens: dict, document: dict) -> WrappedData[Island]:
        logger.debug("[IslandDAO] patching tile data to storage")
        if "id" in document:
            tokens["island_id"] = document["id"]
        island_metadata_path: Path = self._document_path(tokens=tokens)
        if not island_metadata_path.parents[2].exists():
            raise DaoDoesNotExistError("island container (world) does not exist")
        if not island_metadata_path.parent.exists():
            logger.debug("[IslandDAO] island metadata folder creating ..")
            island_metadata_path.parent.mkdir(parents=True, exist_ok=True)

        previous_state: WrappedData[Island] = await self.get(tokens=tokens)
        previous_state.data = Island.model_validate(previous_state.data)

        # if we made it this far we are safe to update

        # merge
        nonce: str = str(uuid.uuid4())
        previous_state_dict = previous_state.data.model_dump()
        new_state = IslandDao.recursive_dict_merge(previous_state_dict, document)
        wrapped_data: WrappedData[Island] = WrappedData[Island](data=new_state, nonce=nonce)

        # serialize to storage
        wrapped_data_raw: str = wrapped_data.model_dump_json(exclude_none=True)
        with open(file=island_metadata_path, mode="w", encoding="utf-8") as file:
            file.write(wrapped_data_raw)
            os.fsync(file)

        # now validate we stored
        stored_entity: WrappedData[Island] = await self.get(tokens=tokens)
        stored_entity.data = Island.model_validate(stored_entity.data)
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
