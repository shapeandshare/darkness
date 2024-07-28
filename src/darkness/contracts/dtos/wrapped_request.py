""" Wrapped Request Definition """

from typing import Any, Optional

from pydantic import BaseModel

from ..types.request_verb import RequestVerbType

# from rowantree.contracts import BaseModel
#
# from ...contracts.request_verb import RequestVerb
from .request_status_codes import RequestStatusCodes


class WrappedRequest(BaseModel):
    """
    Wrapped Request DTO

    Attributes
    ----------
    verb: RequestVerb
        The verb of the REST API request.
    statuses: RequestStatusCodes
        The status code assignments for response handling.
    url: str
        The complete url to call
    data: Optional[Any]  # str or dict ? - needs confirmation
        Either form data or body (based on type - see requests documentation)
    params: Optional[dict[str, str]]
        Query parameters
    """

    verb: RequestVerbType
    statuses: RequestStatusCodes
    url: str
    data: Optional[dict]
    params: Optional[dict[str, str]]
