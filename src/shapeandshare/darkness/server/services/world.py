import logging
import shutil
import uuid
from pathlib import Path

from ...sdk.contracts.dtos.sdk.wrapped_data import WrappedData
from ...sdk.contracts.dtos.world_lite import WorldLite

logger = logging.getLogger()


class WorldService:
    # ["base"]  / "worlds" / "world_id" / metadata.json
    storage_base_path: Path

    def _world_metadata_path(self, world_id: str) -> Path:
        # ["base"] / "worlds" / "world_id" / metadata.json
        return self.storage_base_path / "worlds" / world_id / "metadata.json"

    ### Internal ##################################

    def generate(self, name: str | None) -> str:
        logger.debug("[WorldService] generating world skeleton")
        if name is None:
            name = "darkness"
        world: WorldLite = WorldLite(id=str(uuid.uuid4()), name=name)
        self.post(world=world)
        return world.id

    def get(self, world_id: str) -> WrappedData[WorldLite]:
        logger.debug("[WorldService] getting world metadata from storage")
        world_metadata_path: Path = self._world_metadata_path(world_id=world_id)
        if not world_metadata_path.exists():
            raise Exception("[WorldService] world metadata does not exist - 404, not found, put or patch instead?")
        with open(file=world_metadata_path.resolve().as_posix(), mode="r", encoding="utf-8") as file:
            json_data: str = file.read()
        return WrappedData[WorldLite].model_validate_json(json_data)

    def post(self, world: WorldLite) -> None:
        logger.debug("[WorldService] posting world metadata to storage")
        world_metadata_path: Path = self._world_metadata_path(world_id=world.id)
        if world_metadata_path.exists():
            raise Exception("[WorldService] world metadata already exists - 403, conflict, put or patch instead?")
        if not world_metadata_path.parent.exists():
            logger.debug("[WorldService] world metadata folder creating ..")
            world_metadata_path.parent.mkdir(parents=True, exist_ok=True)

        nonce: str = str(uuid.uuid4())
        wrapped_data: WrappedData[WorldLite] = WrappedData[WorldLite](data=world, nonce=nonce)
        wrapped_data_raw: str = wrapped_data.model_dump_json(indent=4)
        with open(file=world_metadata_path.resolve().as_posix(), mode="w", encoding="utf-8") as file:
            file.write(wrapped_data_raw)

        # now validate we stored
        stored_world: WrappedData[WorldLite] = self.get(world_id=world.id)
        if stored_world.nonce != nonce:
            raise Exception(
                f"[WorldService] Storage inconsistency detected while storing world {world.id} - nonce mismatch!"
            )

    def put(self, world: WorldLite) -> None:
        logger.debug("[WorldService] putting world metadata to storage")
        world_metadata_path: Path = self._world_metadata_path(world_id=world.id)
        if not world_metadata_path.parent.exists():
            logger.debug("[WorldService] world metadata folder creating ..")
            world_metadata_path.parent.mkdir(parents=True, exist_ok=True)

        nonce: str = str(uuid.uuid4())
        wrapped_data: WrappedData[WorldLite] = WrappedData[WorldLite](data=world, nonce=nonce)
        wrapped_data_raw: str = wrapped_data.model_dump_json(indent=4)
        with open(file=world_metadata_path.resolve().as_posix(), mode="w", encoding="utf-8") as file:
            file.write(wrapped_data_raw)

        # now validate we stored
        stored_world: WrappedData[WorldLite] = self.get(world_id=world.id)
        if stored_world.nonce != nonce:
            raise Exception(
                f"[WorldService] Storage inconsistency detected while storing world {world.id} - nonce mismatch!"
            )

    def delete(self, world_id: str) -> None:
        logger.debug("[WorldService] deleting world data from storage")
        world_metadata_path: Path = self._world_metadata_path(world_id=world_id)
        if not world_metadata_path.exists():
            raise Exception("[WorldService] world metadata does not exist - 404, not found")
        # remove "world_id"/ and lower
        shutil.rmtree(world_metadata_path.parent.resolve().as_posix())

    # def _generate(self):
    #     logger.debug("[WorldService] generating world skeleton")
    #     self.world = WorldFactory.generate()
    #
    # def _read(self) -> None:
    #     logger.debug("[WorldService] loading world data from storage")
    #     try:
    #         if self.world:
    #             del self.world
    #             self.world = None
    #         self.world = World.parse_file(path=METADATA_PATH)
    #     except json.decoder.JSONDecodeError as error:
    #         error_message: str = f"[WorldService] Unable to load world data from ({METADATA_PATH})"
    #         logger.error(error_message)
    #         raise ServiceError(error_message) from error
    #
    # def _commit(self):
    #     logger.debug("[WorldService] writing world data to storage")
    #     world_data: str = self.world.model_dump_json(indent=4)
    #     with open(file=METADATA_PATH.resolve().as_posix(), mode="w", encoding="utf-8") as file:
    #         file.write(world_data)
    #
    # ### Islands ##################################
    #
    # def island_create(self, request: IslandCreateRequest) -> str:
    #     logger.debug("[WorldService] creating island")
    #     # discover an island and return its id.
    #     island_id: str = WorldFactory.island_discover(
    #         target_world=self.world, dimensions=request.dimensions, biome=request.biome
    #     )
    #     self._commit()
    #     return island_id
    #
    # def island_delete(self, id: str) -> None:
    #     msg: str = f"[WorldService] deleting island {id}"
    #     logger.debug(msg)
    #     if id in self.world.islands:
    #         del self.world.islands[id]
    #     self._commit()
    #
    # def island_get(self, id: str) -> Island:
    #     msg: str = f"[WorldService] getting island {id}"
    #     logger.debug(msg)
    #
    #     try:
    #         island: Island = self.world.islands[id]
    #     except KeyError as error:
    #         msg: str = f"Unable to find island {id}"
    #         logger.error(msg)
    #         raise ServiceError(msg) from error
    #     return island
    #
    # def island_put(self, island: Island) -> None:
    #     msg: str = f"[WorldService] putting island {island.id} into world storage"
    #     logger.debug(msg)
    #     self.world.islands[island.id] = island
    #     self._commit()
    #
    # def islands_get(self) -> list[str]:
    #     results = [key for key in self.world.islands.keys()]
    #     print(results)
    #     return results
