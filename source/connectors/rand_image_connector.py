#  Copyright (C) 2022
#  Moscow
#  PUBLISHED MATERIAL.
#
#  Authors: Vasiliev Ivan <open.source.can1can@gmail.com>
#
import logging
from typing import Dict

from aiohttp import ClientSession

from utils.aiohttp_wrapper import AIOHttpClientWrapper

logger = logging.getLogger(__name__)


class RandomImageConnector(AIOHttpClientWrapper):
    def __init__(self,
                 server_address: str,
                 default_timeout: int = 10,
                 session: ClientSession = None):
        self._server_address = server_address
        super().__init__(default_timeout=default_timeout, session=session)

    async def get_image(self, width: int = 200, height: int = 300) -> bytes:
        result = await self.make_get(f"{self._server_address}/{width}/{height}", raw_answer=True)
        return result

    def _construct_headers(self) -> Dict[str, str]:
        headers = {"Connection": "Keep-Alive"}
        return headers
