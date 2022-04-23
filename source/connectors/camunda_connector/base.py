#  Copyright (C) 2022
#  Moscow
#  PUBLISHED MATERIAL.
#
#  Authors: Mike Orlov <open.source.can1can@gmail.com>
#
import datetime
import logging
from typing import Dict, Any

from aiohttp import ClientSession

from connectors.camunda_connector.defs import python_type_to_java_type_name
from connectors.camunda_connector.utils import to_java_str, to_java_datetime_str, to_java_date_str
from utils.aiohttp_wrapper import AIOHttpClientWrapper

logger = logging.getLogger(__file__)


class BaseCamundaConnector(AIOHttpClientWrapper):
    def __init__(self,
                 server_address: str,
                 default_timeout: int = 10,
                 session: ClientSession = None):

        self._server_address = server_address
        super().__init__(default_timeout=default_timeout, session=session)

    async def get(self, path: str, query_params: Dict[str, Any] = None):
        prepared_query_params = self._prepare_query_params(query_params)
        url = f'{self._server_address}{path}'
        logger.debug(f'GET {url} {query_params}')
        return await self.make_get(url, headers=self._construct_headers(), params=prepared_query_params)

    async def post(self, path: str, query_params: Dict[str, Any] = None, body_params: Dict[str, Any] = None):
        body_params = body_params if body_params else {}
        url = f'{ self._server_address}{path}'
        logger.debug(f'POST {url} {query_params} {body_params}')
        return await self.make_post(url, headers=self._construct_headers(), json=body_params)

    @staticmethod
    def pack_variables(variables: dict) -> dict:
        result = {}
        for var, val in variables.items():
            java_type_name = python_type_to_java_type_name.get(type(val))
            if java_type_name is None:
                raise ValueError(f'failed to send variable - {var}: {val}, type: {type(val)}')

            if isinstance(val, datetime.datetime):
                val = to_java_datetime_str(val)
            if isinstance(val, datetime.date):
                val = to_java_date_str(val)
            result[var] = {"value": val, "type": java_type_name}
        return result

    def _prepare_query_params(self, query_params: Dict[str, Any] = None):
        if query_params is None:
            query_params = {}
        return {key: to_java_str(value) for key, value in query_params.items()}

    @staticmethod
    def unpack_variables(packed_variables: dict) -> dict:
        return {name: description['value'] for name, description in packed_variables.items()}

    @staticmethod
    def _construct_headers() -> Dict[str, str]:
        headers = {"Connection": "Keep-Alive"}
        return headers
