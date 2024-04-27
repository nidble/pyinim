import asyncio
import time
from typing import cast

from cloud.types.token import Token
from cloud.resolver import CloudResolver

from . import abc as inim_abc

TOKEN_EXPIRATION_TIME = 86400 * 7 # 60 * 60 * 24 * 7 =  7 days < 2 months

class InimAuth():
    def __init__(self, inim: inim_abc.InimAPI):
        self._inim = inim
        self.expires_at = 0
        self._token = None

    async def get_token(self) -> str:
        if not self.valid_token():
            _, _, resp = await self._inim.get_token()
            self._token = resp.Data.Token
            self.expires_at = time.time() + TOKEN_EXPIRATION_TIME

        return self._token

    def valid_token(self) -> bool:
        return cast(float, self.expires_at) > time.time()

