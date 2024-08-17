from ..sdk.contracts.dtos.sdk.command_options import CommandOptions
from ..sdk.contracts.dtos.sdk.requests.chunk.create import ChunkCreateRequest
from ..sdk.contracts.dtos.sdk.requests.chunk.delete import ChunkDeleteRequest
from ..sdk.contracts.dtos.sdk.requests.chunk.get import ChunkGetRequest
from ..sdk.contracts.dtos.sdk.requests.world.create import WorldCreateRequest
from ..sdk.contracts.dtos.sdk.requests.world.delete import WorldDeleteRequest
from ..sdk.contracts.dtos.sdk.requests.world.get import WorldGetRequest
from ..sdk.contracts.dtos.sdk.responses.chunk.create import ChunkCreateResponse
from ..sdk.contracts.dtos.sdk.responses.chunk.get import ChunkGetResponse
from ..sdk.contracts.dtos.sdk.responses.world.create import WorldCreateResponse
from ..sdk.contracts.dtos.sdk.responses.world.get import WorldGetResponse
from ..sdk.contracts.dtos.tiles.chunk import Chunk
from ..sdk.contracts.dtos.tiles.world import World
from ..sdk.contracts.types.tile import TileType
from .commands.chunk.create import ChunkCreateCommand
from .commands.chunk.delete import ChunkDeleteCommand
from .commands.chunk.get import ChunkGetCommand
from .commands.metrics.health.get import HealthGetCommand
from .commands.world.create import WorldCreateCommand
from .commands.world.delete import WorldDeleteCommand
from .commands.world.get import WorldGetCommand


class Client:
    # metrics/health
    health_get_command: HealthGetCommand

    # chunk
    chunk_create_command: ChunkCreateCommand
    chunk_delete_command: ChunkDeleteCommand
    chunk_get_command: ChunkGetCommand

    # world
    world_create_command: WorldCreateCommand
    world_get_command: WorldGetCommand
    world_delete_command: WorldDeleteCommand

    def __init__(self, options: CommandOptions | None = None):
        command_dict: dict = {}
        if options:
            command_dict["options"] = options

        ### metrics
        self.health_get_command = HealthGetCommand.model_validate(command_dict)

        ### chunk
        self.chunk_create_command = ChunkCreateCommand.model_validate(command_dict)
        self.chunk_delete_command = ChunkDeleteCommand.model_validate(command_dict)
        self.chunk_get_command = ChunkGetCommand.model_validate(command_dict)

        # world
        self.world_create_command = WorldCreateCommand.model_validate(command_dict)
        self.world_get_command = WorldGetCommand.model_validate(command_dict)
        self.world_delete_command = WorldDeleteCommand.model_validate(command_dict)

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

    # chunk

    async def chunk_create(self, world_id: str, name: str | None, dimensions: tuple[int, int], biome: TileType) -> str:
        request: ChunkCreateRequest = ChunkCreateRequest(
            world_id=world_id, name=name, dimensions=dimensions, biome=biome
        )
        response: ChunkCreateResponse = await self.chunk_create_command.execute(request=request)
        return response.id

    async def chunk_get(self, world_id: str, chunk_id: str, full: bool = False) -> Chunk:
        request: ChunkGetRequest = ChunkGetRequest(world_id=world_id, chunk_id=chunk_id, full=full)
        response: ChunkGetResponse = await self.chunk_get_command.execute(request=request)
        return response.chunk

    async def chunk_delete(self, world_id: str, chunk_id: str) -> None:
        request: ChunkDeleteRequest = ChunkDeleteRequest(world_id=world_id, chunk_id=chunk_id)
        await self.chunk_delete_command.execute(request=request)

    # world

    async def world_create(self, name: str | None) -> str:
        request: WorldCreateRequest = WorldCreateRequest(name=name)
        response: WorldCreateResponse = await self.world_create_command.execute(request)
        return response.id

    async def world_delete(self, world_id: str) -> None:
        request: WorldDeleteRequest = WorldDeleteRequest(world_id=world_id)
        await self.world_delete_command.execute(request=request)

    async def world_get(self, world_id: str, full: bool) -> World:
        request: WorldGetRequest = WorldGetRequest(world_id=world_id, full=full)
        response: WorldGetResponse = await self.world_get_command.execute(request)
        return response.world
