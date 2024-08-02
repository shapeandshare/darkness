""" Abstract Command Definition """

import json
import logging
import time
from abc import abstractmethod

import requests
from pydantic import BaseModel
from requests import Response

from ...common.config.environment import demand_env_var, demand_env_var_as_float, demand_env_var_as_int
from ...contracts.dtos.command_options import CommandOptions
from ...contracts.dtos.wrapped_request import WrappedRequest
from ...contracts.errors.exceeded_retry_count import ExceededRetryCountError
from ...contracts.errors.request_failure import RequestFailureError
from ...contracts.types.request_verb import RequestVerbType


class AbstractCommand(BaseModel):
    options: CommandOptions | None = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.options is None:
            self.options: CommandOptions = CommandOptions(
                sleep_time=demand_env_var_as_float(name="DARKNESS_SERVICE_SLEEP_TIME"),
                retry_count=demand_env_var_as_int(name="DARKNESS_SERVICE_RETRY_COUNT"),
                tld=demand_env_var(name="DARKNESS_TLD"),
                timeout=demand_env_var_as_float(name="DARKNESS_SERVICE_TIMEOUT"),
            )

    @abstractmethod
    def execute(self, *args, **kwargs) -> any:
        """Command entry point"""

    def _build_requests_params(self, request: WrappedRequest) -> dict:
        """
        Builds the `requests` call parameters.

        Parameters
        ----------
        request: WrappedRequest
            The request to make.

        Returns
        -------
        params: dict
            A dictionary suitable for splatting into the `requests` call.
        """

        params: dict = {
            "url": request.url,
            "timeout": self.options.timeout,
        }
        if request.verb == RequestVerbType.POST:
            params["json"] = request.data
        if request.params is not None:
            params["params"] = request.params
        return params

    def _api_caller(self, request: WrappedRequest, depth: int) -> dict | None:
        """
        Wrapper for calls with `requests` to external APIs.

        Parameters
        ----------
        request: WrappedRequest
            Request to make.
        depth: int
            Call depth of the recursive call (retry)

        Returns
        -------
        response: dict
            A dictionary of the response.
        """

        if depth < 1:
            raise ExceededRetryCountError(json.dumps({"request": request.dict(), "depth": depth}))
        depth -= 1

        params: dict = self._build_requests_params(request=request)
        # pylint: disable=broad-except
        try:
            if request.verb == RequestVerbType.GET:
                response: Response = requests.get(**params)
            elif request.verb == RequestVerbType.POST:
                response: Response = requests.post(**params)
            elif request.verb == RequestVerbType.DELETE:
                response: Response = requests.delete(**params)
            else:
                raise Exception("Unknown Verb")
        except requests.exceptions.ConnectionError as error:
            logging.debug("Connection Error (%s) - Retrying.. %i", str(error), depth)
            time.sleep(self.options.sleep_time)
            return self._api_caller(request=request, depth=depth)
        except Exception as error:
            logging.debug("Exception needed to cover: %s", str(error))
            time.sleep(self.options.sleep_time)
            return self._api_caller(request=request, depth=depth)

        if response.status_code in request.statuses.allow:
            if response.content == b"":
                return None
            return response.json()

        if response.status_code in request.statuses.retry:
            time.sleep(self.options.sleep_time)
            return self._api_caller(request=request, depth=depth)

        if response.status_code in request.statuses.reauth:
            self._authenticate()
            return self._api_caller(request=request, depth=depth)

        raise RequestFailureError(
            json.dumps(
                {
                    "status_code": response.status_code,
                    "request": request.dict(),
                    "depth": depth,
                }
            )
        )

    def wrapped_request(self, request: WrappedRequest) -> dict | None:
        """
        High level request method.  Entry point for consumption.


        Parameters
        ----------
        request: WrappedRequest
            The request to make.

        Returns
        -------
        response: dict
            The response as a dictionary.
        """

        return self._api_caller(request=request, depth=self.options.retry_count)
