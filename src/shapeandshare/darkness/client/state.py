"""" State Service Client Module """

from ..sdk.contracts.dtos.entities.entity import Entity
from ..sdk.contracts.dtos.sdk.command_options import CommandOptions
from ..sdk.contracts.dtos.sdk.requests.chunk.create import ChunkCreateRequest
from ..sdk.contracts.dtos.sdk.requests.chunk.delete import ChunkDeleteRequest
from ..sdk.contracts.dtos.sdk.requests.chunk.get import ChunkGetRequest
from ..sdk.contracts.dtos.sdk.requests.chunk.patch import ChunkPatchRequest
from ..sdk.contracts.dtos.sdk.requests.chunk.quantum import ChunkQuantumRequest
from ..sdk.contracts.dtos.sdk.requests.entity.delete import EntityDeleteRequest
from ..sdk.contracts.dtos.sdk.requests.entity.entity import EntityRequest
from ..sdk.contracts.dtos.sdk.requests.entity.patch import EntityPatchRequest
from ..sdk.contracts.dtos.sdk.requests.tile.delete import TileDeleteRequest
from ..sdk.contracts.dtos.sdk.requests.tile.get import TileGetRequest
from ..sdk.contracts.dtos.sdk.requests.tile.patch import TilePatchRequest
from ..sdk.contracts.dtos.sdk.requests.world.create import WorldCreateRequest
from ..sdk.contracts.dtos.sdk.requests.world.delete import WorldDeleteRequest
from ..sdk.contracts.dtos.sdk.requests.world.get import WorldGetRequest
from ..sdk.contracts.dtos.sdk.requests.world.patch import WorldPatchRequest
from ..sdk.contracts.dtos.sdk.responses.chunk.create import ChunkCreateResponse
from ..sdk.contracts.dtos.sdk.responses.chunk.get import ChunkGetResponse
from ..sdk.contracts.dtos.sdk.responses.entity.get import EntityGetResponse
from ..sdk.contracts.dtos.sdk.responses.tile.get import TileGetResponse
from ..sdk.contracts.dtos.sdk.responses.world.create import WorldCreateResponse
from ..sdk.contracts.dtos.sdk.responses.world.get import WorldGetResponse
from ..sdk.contracts.dtos.sdk.responses.worlds.get import WorldsGetResponse
from ..sdk.contracts.dtos.tiles.chunk import Chunk
from ..sdk.contracts.dtos.tiles.tile import Tile
from ..sdk.contracts.dtos.tiles.world import World
from ..sdk.contracts.types.chunk_quantum import ChunkQuantumType
from ..sdk.contracts.types.tile import TileType
from .commands.chunk.create import ChunkCreateCommand
from .commands.chunk.delete import ChunkDeleteCommand
from .commands.chunk.get import ChunkGetCommand
from .commands.chunk.patch import ChunkPatchCommand
from .commands.chunk.quantum import ChunkQuantumCommand
from .commands.entity.delete import EntityDeleteCommand
from .commands.entity.get import EntityGetCommand
from .commands.entity.patch import EntityPatchCommand
from .commands.metrics.health.get import HealthGetCommand
from .commands.tile.delete import TileDeleteCommand
from .commands.tile.get import TileGetCommand
from .commands.tile.patch import TilePatchCommand
from .commands.world.create import WorldCreateCommand
from .commands.world.delete import WorldDeleteCommand
from .commands.world.get import WorldGetCommand
from .commands.world.patch import WorldPatchCommand
from .commands.worlds.get import WorldsGetCommand


# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments
# pylint: disable=too-many-public-methods
class StateClient:
    # metrics/health
    health_get_command: HealthGetCommand

    # entity
    entity_delete_command: EntityDeleteCommand
    entity_get_command: EntityGetCommand
    entity_patch_command: EntityPatchCommand

    # tile
    tile_delete_command: TileDeleteCommand
    tile_get_command: TileGetCommand
    tile_patch_command: TilePatchCommand

    # chunk
    chunk_create_command: ChunkCreateCommand
    chunk_delete_command: ChunkDeleteCommand
    chunk_get_command: ChunkGetCommand
    chunk_patch_command: ChunkPatchCommand
    chunk_quantum_command: ChunkQuantumCommand

    # world
    world_create_command: WorldCreateCommand
    world_delete_command: WorldDeleteCommand
    world_get_command: WorldGetCommand
    world_patch_command: WorldPatchCommand

    # worlds
    worlds_get_command: WorldsGetCommand

    def __init__(self, options: CommandOptions | None = None):
        command_dict: dict = {}
        if options:
            command_dict["options"] = options

        ### metrics
        self.health_get_command = HealthGetCommand.model_validate(command_dict)

        ## entity
        self.entity_delete_command = EntityDeleteCommand.model_validate(command_dict)
        self.entity_get_command = EntityGetCommand.model_validate(command_dict)
        self.entity_patch_command = EntityPatchCommand.model_validate(command_dict)

        ## tile
        self.tile_delete_command = TileDeleteCommand.model_validate(command_dict)
        self.tile_get_command = TileGetCommand.model_validate(command_dict)
        self.tile_patch_command = TilePatchCommand.model_validate(command_dict)

        ### chunk
        self.chunk_create_command = ChunkCreateCommand.model_validate(command_dict)
        self.chunk_delete_command = ChunkDeleteCommand.model_validate(command_dict)
        self.chunk_get_command = ChunkGetCommand.model_validate(command_dict)
        self.chunk_patch_command = ChunkPatchCommand.model_validate(command_dict)
        self.chunk_quantum_command = ChunkQuantumCommand.model_validate(command_dict)

        # world
        self.world_create_command = WorldCreateCommand.model_validate(command_dict)
        self.world_delete_command = WorldDeleteCommand.model_validate(command_dict)
        self.world_get_command = WorldGetCommand.model_validate(command_dict)
        self.world_patch_command = WorldPatchCommand.model_validate(command_dict)

        # worlds
        self.worlds_get_command = WorldsGetCommand.model_validate(command_dict)

    # metrics

    async def health_get(self) -> dict:
        """
        Gets the server health.

        Returns
        -------
        health: dict
            The server health (true or false).
        """

        return await self.health_get_command.execute()

    # entity
    async def entity_delete(self, world_id: str, chunk_id: str, tile_id: str, entity_id: str, parent: bool) -> bool:
        request: EntityDeleteRequest = EntityDeleteRequest(
            world_id=world_id, chunk_id=chunk_id, tile_id=tile_id, entity_id=entity_id, parent=parent
        )
        success: bool = await self.entity_delete_command.execute(request=request)
        return success

    async def entity_get(self, world_id: str, chunk_id: str, tile_id: str, entity_id: str) -> Entity:
        request: EntityRequest = EntityRequest(
            world_id=world_id, chunk_id=chunk_id, tile_id=tile_id, entity_id=entity_id
        )
        response: EntityGetResponse = await self.entity_get_command.execute(request=request)
        return response.data

    async def entity_patch(self, world_id: str, chunk_id: str, tile_id: str, entity_id: str, partial: dict) -> bool:
        request: EntityPatchRequest = EntityPatchRequest(
            world_id=world_id, chunk_id=chunk_id, tile_id=tile_id, entity_id=entity_id, partial=partial
        )
        success: bool = await self.entity_patch_command.execute(request=request)
        return success

    # tile
    async def tile_delete(self, world_id: str, chunk_id: str, tile_id: str, parent: bool, cascade: bool) -> bool:
        request: TileDeleteRequest = TileDeleteRequest(
            world_id=world_id, chunk_id=chunk_id, tile_id=tile_id, parent=parent, cascade=cascade
        )
        success: bool = await self.tile_delete_command.execute(request=request)
        return success

    async def tile_get(self, world_id: str, chunk_id: str, tile_id: str, full: bool) -> Tile:
        request: TileGetRequest = TileGetRequest(world_id=world_id, chunk_id=chunk_id, tile_id=tile_id, full=full)
        response: TileGetResponse = await self.tile_get_command.execute(request=request)
        return response.tile

    async def tile_patch(self, world_id: str, chunk_id: str, tile_id: str, partial: dict) -> bool:
        request: TilePatchRequest = TilePatchRequest(
            world_id=world_id, chunk_id=chunk_id, tile_id=tile_id, partial=partial
        )
        success: bool = await self.tile_patch_command.execute(request=request)
        return success

    # chunk

    async def chunk_create(self, world_id: str, name: str | None, dimensions: tuple[int, int], biome: TileType) -> str:
        request: ChunkCreateRequest = ChunkCreateRequest(
            world_id=world_id, name=name, dimensions=dimensions, biome=biome
        )
        response: ChunkCreateResponse = await self.chunk_create_command.execute(request=request)
        return response.id

    async def chunk_delete(self, world_id: str, chunk_id: str, parent: bool, cascade: bool) -> bool:
        request: ChunkDeleteRequest = ChunkDeleteRequest(
            world_id=world_id, chunk_id=chunk_id, parent=parent, cascade=cascade
        )
        success: bool = await self.chunk_delete_command.execute(request=request)
        return success

    async def chunk_get(self, world_id: str, chunk_id: str, full: bool = False) -> Chunk:
        request: ChunkGetRequest = ChunkGetRequest(world_id=world_id, chunk_id=chunk_id, full=full)
        response: ChunkGetResponse = await self.chunk_get_command.execute(request=request)
        return response.chunk

    async def chunk_patch(self, world_id: str, chunk_id: str, partial: dict) -> bool:
        request: ChunkPatchRequest = ChunkPatchRequest(world_id=world_id, chunk_id=chunk_id, partial=partial)
        success: bool = await self.chunk_patch_command.execute(request=request)
        return success

    async def chunk_quantum(self, world_id: str, chunk_id: str, scope: ChunkQuantumType) -> None:
        request: ChunkQuantumRequest = ChunkQuantumRequest(world_id=world_id, chunk_id=chunk_id, scope=scope)
        await self.chunk_quantum_command.execute(request=request)

    # world

    async def world_create(self, name: str | None) -> str:
        request: WorldCreateRequest = WorldCreateRequest(name=name)
        response: WorldCreateResponse = await self.world_create_command.execute(request)
        return response.id

    async def world_delete(self, world_id: str, cascade: bool) -> bool:
        request: WorldDeleteRequest = WorldDeleteRequest(world_id=world_id, cascade=cascade)
        success: bool = await self.world_delete_command.execute(request=request)
        return success

    async def world_get(self, world_id: str, full: bool) -> World:
        request: WorldGetRequest = WorldGetRequest(world_id=world_id, full=full)
        response: WorldGetResponse = await self.world_get_command.execute(request)
        return response.world

    async def world_patch(self, world_id: str, partial: dict) -> bool:
        request: WorldPatchRequest = WorldPatchRequest(world_id=world_id, partial=partial)
        success: bool = await self.world_patch_command.execute(request=request)
        return success

    # worlds

    async def worlds_get(self) -> list[World]:
        response: WorldsGetResponse = await self.worlds_get_command.execute()
        return response.worlds
