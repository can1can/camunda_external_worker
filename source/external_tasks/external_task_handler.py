#  Copyright (C) 2022
#  Moscow
#  PUBLISHED MATERIAL.
#
#  Authors: Vasiliev Ivan <open.source.can1can@gmail.com>
#
import logging
from abc import ABC, abstractmethod

from dataclasses import dataclass, field
from typing import Optional

from connectors.camunda_connector.defs import ExternalTask
from custom_exeption import CamundaError, TaskHandlingError
from connectors.camunda_connector.connector import CamundaConnector
logger = logging.getLogger(__name__)


@dataclass
class ExternalTaskResult:
    pass


@dataclass
class ExternalTaskSuccess(ExternalTaskResult):
    variables: dict = field(default_factory=dict)


@dataclass
class Failure(ExternalTaskResult):
    retries: Optional[int] = None
    retry_timeout: Optional[int] = 8000
    msg: Optional[str] = None
    pass


class AbstractExternalTaskHandler(ABC):
    class Context:
        camunda_connector: CamundaConnector = None

    def __init__(self,  context: Context, topic_name: str, worker_id: str, lock_duration: int = 70000):
        self.context = context
        self.topic_name = topic_name
        self.__worker_id = worker_id
        self.__lock_duration = lock_duration

    @abstractmethod
    async def _handle_task(self, camunda_task: ExternalTask, topic_args: dict) -> ExternalTaskResult:
        pass

    async def process_camunda_task(self, camunda_task: ExternalTask):
        try:
            topic_args = await self._get_args_and_lock(camunda_task)
        except CamundaError:
            return
        try:
            task_result = await self._handle_task(camunda_task, topic_args)
        except TaskHandlingError as e:
            task_result = Failure(msg=repr(e))

        await self._processed_task_result(camunda_task, task_result, topic_args)

    async def _get_args_and_lock(self, camunda_task: ExternalTask) -> dict:
        try:
            topic_args = await self.context.camunda_connector.process.get_process_variables(
                camunda_task.process_instance_id)
            logger.debug(f"task: {camunda_task.id}, {camunda_task.process_instance_id} args {topic_args} ")

            # TODO for horizontal scaling check if it's possible to set different worker_id for different instances
            await self.context.camunda_connector.external_task.lock(camunda_task.id, self.__worker_id,
                                                                    lock_duration_ms=self.__lock_duration)
            logger.debug(f"task: {camunda_task.id} locked ")
            return topic_args
        except Exception as e:
            logger.warning(f"task: {camunda_task}; camunda error: {repr(e)}")
            raise CamundaError(repr(e))

    async def _processed_task_result(self, camunda_task: ExternalTask, task_result: ExternalTaskResult, topic_args):
        if isinstance(task_result, Failure):
            await self._process_failure(camunda_task, task_result)
        elif isinstance(task_result, ExternalTaskSuccess):
            try:
                await self.context.camunda_connector.external_task.complete(task_id=camunda_task.id,
                                                                            worker_id=self.__worker_id,
                                                                            variables=task_result.variables)
            except Exception as e:
                logger.warning(f"task: {camunda_task}; camunda error: {repr(e)}")

    async def _process_failure(self, task: ExternalTask, failure: Failure):

        try:
            logger.debug(f"proceeding failure for task {task.id} ")
            await self.context.camunda_connector.external_task.failure(task.id,
                                                                       worker_id=self.__worker_id,
                                                                       retry_timeout=failure.retry_timeout,
                                                                       retries=failure.retries,
                                                                       error_message=failure.msg)
            logger.info(f"failure for task {task.id} reported")
        # Todo add Exception separation
        except Exception as e:
            logger.info(f"report failure for task {task.id} failed: {e}")
