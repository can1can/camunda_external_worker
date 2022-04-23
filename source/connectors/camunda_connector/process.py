#  Copyright (C) 2022
#  Moscow
#  PUBLISHED MATERIAL.
#
#  Authors: Vasiliev Ivan <open.source.can1can@gmail.com>
#
from typing import List, Optional, Dict

from .base import BaseCamundaConnector


class ProcessConnector:

    def __init__(self, connector: BaseCamundaConnector):
        self.camunda = connector

    async def get_process_variables(self, process_id):
        process_variables = await self.camunda.get(f'/process-instance/{process_id}/variables')
        return self.camunda.unpack_variables(process_variables)

    async def get_variables_by_activity_instance_id(self, activity_instance_id: str) -> dict:
        body_params = {"activityInstanceIdIn": [activity_instance_id]}
        process_variable_descriptions = await self.camunda.post(f'/variable-instance', body_params=body_params)
        result = {description["name"]: description["value"] for description in process_variable_descriptions}
        return result
