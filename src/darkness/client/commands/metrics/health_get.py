""" Health Get Command Definition """

import requests

from ....contracts.dtos.responses.response import Response
from ..abstract import AbstractCommand

# from requests import Response



class HealthGetCommand(AbstractCommand):
    """
    Health Get Command
    Gets the server health.

    Methods
    -------
    execute(self) -> bool
        Executes the command.
    """

    def execute(self) -> dict:
        """
        Executes the command.

        Returns
        -------
        health: bool
            The server health (true or false).
        """

        response: requests.Response = requests.get(
            url=f"http://{self.options.tld}/metrics/health",
            timeout=self.options.timeout,
        )
        return Response[dict].parse_obj(response.json()).data
