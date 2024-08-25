""" Health Get Command Definition """

import requests

from .....sdk.contracts.dtos.sdk.responses.response import Response
from ...abstract import AbstractCommand


class HealthGetCommand(AbstractCommand):
    """
    Health Get Command
    Gets the server health.

    Methods
    -------
    execute(self) -> dict
        Executes the command.
    """

    async def execute(self) -> dict:
        """
        Executes the command.

        Returns
        -------
        health: dict
            The server health (true or false).
        """

        response: requests.Response = requests.get(
            url=f"http://{self.options.tld}/metrics/health", timeout=self.options.timeout
        )
        return Response[dict].model_validate(response.json()).data
