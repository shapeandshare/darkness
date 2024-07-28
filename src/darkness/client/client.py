from ..contracts.dtos.command_options import CommandOptions
from .commands.metrics.health_get import HealthGetCommand

# from src.darkness.client.commands.metrics.health_get import HealthGetCommand


class Client:

    health_get_command: HealthGetCommand

    # user_active_get_command: UserActiveGetCommand
    # island_get: IslandGetCommand

    def __init__(self, options: CommandOptions | None = None):
        command_dict: dict = {}
        if options:
            command_dict["options"] = options

        self.health_get_command = HealthGetCommand.parse_obj(command_dict)

    def health_get(self) -> dict:
        """
        Gets the server health.

        Returns
        -------
        health: bool
            The server health (true or false).
        """

        return self.health_get_command.execute()
