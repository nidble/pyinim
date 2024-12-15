"""Provide an abstract base class for easier requests."""

import abc
from typing import Tuple, Mapping
import logging

from pyinim.cloud.exceptions import MalformedResponseError
from pyinim.cloud.resolver import CloudResolver
from pyinim.cloud.types.token import Token
from pyinim.cloud.types.devices import Devices

_LOGGER = logging.getLogger(__name__)

class InimAPI(abc.ABC):
    """Provide an idiomatic API for making calls to Inim's API."""

    def __init__(
        self,
        requester: str,
        *,
        resolver: CloudResolver,
    ) -> None:
        self.requester = requester
        self.resolver = resolver
        # self.rate_limit: Opt[RateLimit] = None

    @abc.abstractmethod
    async def _request(
        self, method: str, url: str, headers: Mapping[str, str], body: bytes = b""
    ) -> Tuple[int, Mapping[str, str], bytes]:
        """Make an HTTP request."""

    @abc.abstractmethod
    async def sleep(self, seconds: float) -> None:
        """Sleep for the specified number of seconds."""

    @abc.abstractmethod
    async def token(self) -> str:
        """Get the token string."""

    async def get_token(self) -> Tuple[int, Mapping[str, str], Token]:
        status, headers, raw_response = await self._request(
            "GET", self.resolver.get_token_url(), headers={}
        )
        parsed_response = self.resolver.str_to_token(raw_response)
        if parsed_response.Data is None:
            raise MalformedResponseError(
                f"Failed to get Token with {status=} and payload {raw_response=}"
            )
        return status, headers, parsed_response

    async def get_request_poll(
        self, device_id: str
    ) -> Tuple[int, Mapping[str, str], None]:
        status, headers, raw_response = await self._request(
            "GET",
            self.resolver.get_request_poll_url(await self.token(), device_id),
            headers={},
        )
        return status, headers, None

    async def get_devices_extended(
        self, device_id: str
    ) -> Tuple[int, Mapping[str, str], Devices]:
        status, headers, raw_response = await self._request(
            "GET",
            self.resolver.get_devices_extended_url(await self.token()),
            headers={},
        )
        try:
            response = self.resolver.str_to_devices(raw_response, device_id)
        except Exception as e:
            message = f"Failed to get Devices with {status=} and payload {raw_response=}"
            _LOGGER.warning(message)
            raise MalformedResponseError(message) from e
        return status, headers, response

    async def get_activate_scenario(
        self, device_id: str, scenario_id: str
    ) -> Tuple[int, Mapping[str, str], str]:
        status, headers, raw_response = await self._request(
            "GET",
            self.resolver.get_activate_scenario_url(
                await self.token(), device_id, scenario_id
            ),
            headers={},
        )
        return status, headers, raw_response

    async def get_devices_list(self) -> dict[str, Devices]:
        """Gets a map of all devices."""
        status, headers, raw_response = await self._request(
            "GET",
            self.resolver.get_devices_extended_url(await self.token()),
            headers={},
        )
        return (
            status,
            headers,
            self.resolver.str_to_devices_list(raw_response),
        )
