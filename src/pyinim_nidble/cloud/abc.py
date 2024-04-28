"""Provide an abstract base class for easier requests."""
import abc
from typing import Optional as Mapping, Tuple, Mapping

from pyinim_nidble.cloud.resolver import CloudResolver
from pyinim_nidble.cloud.types.token import Token
from pyinim_nidble.cloud.types.devices import Devices

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
        status, headers, raw_response = await self._request('GET', self.resolver.get_token_url(), headers={})
        return status, headers, self.resolver.str_to_token(raw_response)

    async def get_request_poll(self, device_id: str) -> Tuple[int, Mapping[str, str], None]:
        status, headers, raw_response = await self._request('GET', self.resolver.get_request_poll_url(await self.token(), device_id), headers={})
        return status, headers, None

    async def get_devices_extended(self, device_id: str) -> Tuple[int, Mapping[str, str], Devices]:
        status, headers, raw_response = await self._request('GET', self.resolver.get_devices_extended_url(await self.token()), headers={})
        return status, headers, self.resolver.str_to_devices(raw_response, device_id)

    async def get_activate_scenario(self, device_id: str, scenario_id: str) -> Tuple[int, Mapping[str, str], str]:
        status, headers, raw_response = await self._request('GET', self.resolver.get_activate_scenario_url(await self.token(), device_id, scenario_id), headers={})
        return status, headers, raw_response
