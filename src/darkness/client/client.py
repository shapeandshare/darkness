from ..contracts.dtos.command_options import CommandOptions
from ..contracts.dtos.requests.island_create_request import IslandCreateRequest
from ..contracts.dtos.responses.island_create_response import IslandCreateResponse
from ..contracts.dtos.responses.response import Response
from ..contracts.types.tile import TileType
from .commands.islands.island_create import IslandCreateCommand
from .commands.metrics.health_get import HealthGetCommand

# from src.darkness.client.commands.metrics.health_get import HealthGetCommand


class Client:
    health_get_command: HealthGetCommand

    island_create_command: IslandCreateCommand

    # user_active_get_command: UserActiveGetCommand
    # island_get: IslandGetCommand

    def __init__(self, options: CommandOptions | None = None):
        command_dict: dict = {}
        if options:
            command_dict["options"] = options

        self.health_get_command = HealthGetCommand.parse_obj(command_dict)

        self.island_create_command = IslandCreateCommand.parse_obj(command_dict)

    def health_get(self) -> dict:
        """
        Gets the server health.

        Returns
        -------
        health: bool
            The server health (true or false).
        """

        return self.health_get_command.execute()

    def island_create(
        self, dim: tuple[int, int], biome: TileType
    ) -> IslandCreateResponse:
        request: IslandCreateRequest = IslandCreateRequest(dim=dim, biome=biome)
        return self.island_create_command.execute(request=request)
