#  Copyright (C) 2022
#  Moscow
#  PUBLISHED MATERIAL.
#
#  Authors: Vasiliev Ivan <open.source.can1can@gmail.com>
#
import logging

from connectors.camunda_connector.connector import CamundaConnector
from connectors.camunda_connector.defs import ExternalTask
from connectors.rand_image_connector import RandomImageConnector
from file_handler import FileHandler
from external_tasks.external_task_handler import AbstractExternalTaskHandler, ExternalTaskResult, \
    ExternalTaskSuccess

logger = logging.getLogger(__name__)


class RandomImageHandler(AbstractExternalTaskHandler):
    class Context:
        camunda_connector: CamundaConnector = None
        image_connector: RandomImageConnector = None
        file_handler: FileHandler = None

    async def _handle_task(self, camunda_task: ExternalTask, topic_args: dict) -> ExternalTaskResult:
        logger.debug(f"handling camunda task: {camunda_task} with args: {topic_args}")
        image = await self.context.image_connector.get_image()
        file_id = await self.context.file_handler.upload(image)
        return ExternalTaskSuccess({"file_id": file_id})
