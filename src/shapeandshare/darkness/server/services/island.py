import logging
import shutil
import uuid
from pathlib import Path

from ... import TileType
from ...sdk.contracts.dtos.island_lite import IslandLite
from ...sdk.contracts.dtos.sdk.wrapped_data import WrappedData

logger = logging.getLogger()


class IslandService:
    # ["base"]  / "worlds" / "world_id" / "islands" / "island_id" / metadata.json
    storage_base_path: Path

    def __init__(self):
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
            raise Exception("[IslandService] island metadata does not exist - 404, not found, put or patch instead?")
        with open(file=island_metadata_path.resolve().as_posix(), mode="r", encoding="utf-8") as file:
            json_data: str = file.read()
        return WrappedData[IslandLite].model_validate_json(json_data)

    def post(self, world_id: str, island: IslandLite) -> None:
        logger.debug("[IslandService] posting island metadata to storage")
        island_metadata_path: Path = self._island_metadata_path(world_id=world_id, island_id=island.id)
        if island_metadata_path.exists():
            raise Exception("[IslandService] island metadata already exists - 403, conflict, put or patch instead?")
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
            raise Exception(
                f"[IslandService] Storage inconsistency detected while storing island {island.id} - nonce mismatch!"
            )

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
            raise Exception(
                f"[IslandService] Storage inconsistency detected while storing island {island.id} - nonce mismatch!"
            )

    def delete(self, world_id: str, island_id: str) -> None:
        logger.debug("[IslandService] deleting island data from storage")
        island_metadata_path: Path = self._island_metadata_path(world_id=world_id, island_id=island_id)
        if not island_metadata_path.exists():
            raise Exception("[IslandService] island metadata does not exist - 404, not found")
        # remove "island_id"/ and lower
        shutil.rmtree(island_metadata_path.parent.resolve().as_posix())

    # def _read(self) -> None:
    #     logger.debug("[IslandService] loading island data from storage")
    #     try:
    #         if self.island:
    #             del self.island
    #             self.island = None
    #         self.island = Island.parse_file(path=METADATA_PATH)
    #     except json.decoder.JSONDecodeError as error:
    #         error_message: str = f"[IslandService] Unable to load island data from ({self.storage_base_path})"
    #         logger.error(error_message)
    #         raise ServiceError(error_message) from error
    #
    # def _commit(self):
    #     logger.debug("[IslandService] writing island data to storage")
    #     island_data: str = self.island.model_dump_json(indent=4)
    #     with open(file=self.storage_base_path.resolve().as_posix(), mode="w", encoding="utf-8") as file:
    #         file.write(island_data)
    #
    # ### Islands ##################################
    #
    # def island_create(self, request: IslandCreateRequest) -> str:
    #     logger.debug("[IslandService] creating island")
    #     # discover an island and return its id.
    #     island_id: str = IslandFactory.island_discover(
    #         target_island=self.island, dimensions=request.dimensions, biome=request.biome
    #     )
    #     self._commit()
    #     return island_id
    #
    # def island_delete(self, id: str) -> None:
    #     msg: str = f"[IslandService] deleting island {id}"
    #     logger.debug(msg)
    #     if id in self.island.islands:
    #         del self.island.islands[id]
    #     self._commit()
    #
    # def island_get(self, id: str) -> Island:
    #     msg: str = f"[IslandService] getting island {id}"
    #     logger.debug(msg)
    #
    #     try:
    #         island: Island = self.island.islands[id]
    #     except KeyError as error:
    #         msg: str = f"Unable to find island {id}"
    #         logger.error(msg)
    #         raise ServiceError(msg) from error
    #     return island
    #
    # def island_put(self, island: Island) -> None:
    #     msg: str = f"[IslandService] putting island {island.id} into island storage"
    #     logger.debug(msg)
    #     self.island.islands[island.id] = island
    #     self._commit()
    #
    # # def islands_get(self) -> list[str]:
    # #     results = [key for key in self.island.islands.keys()]
    # #     print(results)
    # #     return results
