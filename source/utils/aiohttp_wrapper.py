#  Copyright (C) 2022
#  Moscow
#  PUBLISHED MATERIAL.
#
#  Authors: Vasiliev Ivan <open.source.can1can@gmail.com>
#
import logging
from typing import Union, Optional

from aiohttp import ClientResponse, web, ClientSession, BasicAuth

logger = logging.getLogger(__name__)


class AIOHttpClientWrapper:
    def __init__(self,
                 default_timeout: int = 10,
                 session: ClientSession = None):
        self.__default_timeout = default_timeout
        if session is None:
            self.__session = ClientSession()
        else:
            self.__session = session

    async def close(self) -> None:
        await self.__session.close()

    async def make_post(self,
                        url: str,
                        params: Optional[dict] = None,
                        json: Union[dict, list, None] = None,
                        data: Optional[bytes] = None,
                        headers: Optional[dict] = None,
                        auth: Optional[BasicAuth] = None,
                        timeout: Optional[int] = None,
                        raw_answer: bool = False) -> Union[dict, list, ClientResponse]:
        if timeout is None:
            timeout = self.__default_timeout
        async with self.__session.post(url, params=params, json=json, data=data,
                                       timeout=timeout, auth=auth,
                                       headers=headers) as resp:
            self._check_response_code(resp)
            if raw_answer:
                await resp.read()
                answer = resp
            else:
                answer = await resp.json(content_type=None)
            return answer

    async def make_get(self,
                       url: str,
                       params: Optional[dict] = None,
                       headers: Optional[dict] = None,
                       auth: Optional[BasicAuth] = None,
                       timeout: Optional[int] = None,
                       raw_answer: bool = False) -> Union[dict, list, ClientResponse, bytes]:
        logger.info(url)
        if timeout is None:
            timeout = self.__default_timeout
        async with self.__session.get(url, params=params, timeout=timeout, auth=auth,
                                      headers=headers) as resp:
            self._check_response_code(resp)
            if raw_answer:
                answer = await resp.read()
            else:
                answer = await resp.json(content_type=None)
            return answer
    @staticmethod
    def _check_response_code(resp: ClientResponse) -> None:
        if resp.status == 200 or resp.status == 201 or resp.status == 204 or resp.status == 202:
            return
        if resp.status == 400:
            raise web.HTTPBadRequest(reason=resp._body)
        elif resp.status == 401:
            raise web.HTTPUnauthorized(reason=resp._body)
        elif resp.status == 403:
            raise web.HTTPForbidden(reason=resp._body)
        elif resp.status == 404:
            raise web.HTTPNotFound(reason=resp._body)
        elif resp.status == 422:
            raise web.HTTPUnprocessableEntity(reason=resp._body)
        elif resp.status == 503 or resp.status == 500:
            raise web.HTTPServiceUnavailable(reason=resp._body)
        else:
            logger.warning("unknown code: %s", resp.status)
            raise web.HTTPInternalServerError(reason=resp._body)
