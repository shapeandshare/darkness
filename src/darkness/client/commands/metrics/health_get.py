""" Health Get Command Definition """

import requests
from requests import Response

from ..abstract import AbstractCommand


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

        response: Response = requests.get(
            url=f"http://{self.options.tld}/metrics/health",
            timeout=self.options.timeout,
        )
        return {"status": response.status_code, "data": response.text}
