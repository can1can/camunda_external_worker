#  Copyright (C) 2022
#  Moscow
#  PUBLISHED MATERIAL.
#
#  Authors: Vasiliev Ivan <open.source.can1can@gmail.com>
#
import logging

from connectors.camunda_connector.defs import ExternalTask
from custom_exeption import TaskHandlingError
from external_tasks.external_task_handler import AbstractExternalTaskHandler, ExternalTaskResult, ExternalTaskSuccess
from file_handler import FileHandler
logger = logging.getLogger(__name__)


class WaterMarkHandler(AbstractExternalTaskHandler):
    class Context:
        file_handler: FileHandler = None

    async def _handle_task(self, camunda_task: ExternalTask, topic_args: dict) -> ExternalTaskResult:
        logger.info(f"handling camunda task: {camunda_task} with args: {topic_args}")
        image_id = topic_args.get("file_id")
        if not image_id:
            logger.info("raising")
            raise TaskHandlingError("file id required")
        file_content = await self.context.file_handler.load(image_id)
        # logger.info(f"file_content: {file_content}")
        return ExternalTaskSuccess()
