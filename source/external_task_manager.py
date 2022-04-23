#  Copyright (C) 2022
#  Moscow
#  PUBLISHED MATERIAL.
#
#  Authors: Vasiliev Ivan <open.source.can1can@gmail.com>
#
import asyncio
import logging
from dataclasses import dataclass
from typing import List, NoReturn

from connectors.camunda_connector.connector import CamundaConnector
from connectors.camunda_connector.defs import ExternalTask
from external_tasks.external_task_handler import AbstractExternalTaskHandler

logger = logging.getLogger(__file__)


class ExternalTaskManager:
    @dataclass
    class Context:
        camunda_connector: CamundaConnector = None

    def __init__(self,
                 context: Context,
                 ):
        self.camunda_task_connector = context.camunda_connector.external_task
        self.__topic_to_processor = {}
        self.__task_ids = set()

    def register_external_task_handler(self, external_task_handler: AbstractExternalTaskHandler):
        self.__topic_to_processor[external_task_handler.topic_name] = external_task_handler.process_camunda_task

    async def run_monitoring(self) -> NoReturn:
        while True:
            try:
                logger.debug(f"{self.__class__.__name__}: monitoring cycle started.")
                task_list: List[ExternalTask] = await self.camunda_task_connector.get_list()
                # logger.info(f"task_list: {task_list}")
                handle_tasks = []
                for task in task_list:
                    if task.topic_name in self.__topic_to_processor:
                        handle_tasks.append(asyncio.create_task(self.__topic_to_processor[task.topic_name](task)))
                await asyncio.gather(*handle_tasks)
            except Exception as er:
                logger.exception(f"{self.__class__.__name__}.run.error: {repr(er)}")
            #
            # logger.debug(f"{self.__class__.__name__}: monitoring cycle ended.")
            await asyncio.sleep(1)
