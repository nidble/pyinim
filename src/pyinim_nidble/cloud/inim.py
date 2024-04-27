import asyncio
import aiohttp
import time
from typing import Any, Mapping, Tuple, cast

from .auth import InimAuth
from .resolver import CloudResolver

from . import abc as inim_abc

class InimCloudCli(inim_abc.InimAPI):
    def __init__(
        self, session: aiohttp.ClientSession, *args: Any, **kwargs: Any
    ) -> None:
        self._session = session
        resolver = CloudResolver(kwargs['username'], kwargs['password'], kwargs['client_id'])
        # super().__init__(*args, resolver=resolver, **kwargs)
        super().__init__('requester', resolver=resolver)
        self._auth = InimAuth(self)

    async def _request(
        self, method: str, url: str, headers: Mapping[str, str], body: bytes = b""
    ) -> Tuple[int, Mapping[str, str], str]:
        async with self._session.request(
            method, url, headers=headers, data=body
        ) as response:
            return response.status, response.headers, await response.text() # change with await response.read() for bytes

    async def sleep(self, seconds: float) -> None:
        await asyncio.sleep(seconds)

    async def token(self) -> str:
        return await self._auth.get_token()
    