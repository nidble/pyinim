import asyncio
import aiohttp
import time
from typing import Any, Mapping, Tuple, cast

from pyinim.cloud.resolver import CloudResolver
from pyinim.cloud.types.token import Token
from pyinim.cloud import abc

# TOKEN_EXPIRATION_TIME = 86400 * 7 # 60 * 60 * 24 * 7 =  7 days < 2 months
TOKEN_EXPIRATION_TIME = 21600 # 60 * 60 * 6 = every 6 hours

class InimCloud(abc.InimAPI):
    def __init__(
        self, session: aiohttp.ClientSession, *args: Any, **kwargs: Any
    ) -> None:
        self._session = session
        resolver = CloudResolver(kwargs['username'], kwargs['password'], kwargs['client_id'])
        self.name = kwargs['name']
        self.expires_at = 0
        self._token = None

        # super().__init__(*args, resolver=resolver, **kwargs)
        super().__init__(self.name, resolver=resolver)

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
        if not self._valid_token():
            _, _, resp = await self.get_token()
            self._token = resp.Data.Token
            self.expires_at = time.time() + TOKEN_EXPIRATION_TIME

        return self._token

    def _valid_token(self) -> bool:
        return cast(float, self.expires_at) > time.time()
