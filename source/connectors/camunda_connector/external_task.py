#  Copyright (C) 2022
#  Moscow
#  PUBLISHED MATERIAL.
#
#  Authors: Mike Orlov <open.source.can1can@gmail.com>
#
from typing import List, Dict, Any

from .base import BaseCamundaConnector
from connectors.camunda_connector.defs import ExternalTask


class ExternalTaskConnector:
    def __init__(self, connector: BaseCamundaConnector):
        self.camunda = connector

    async def get_list(self, skip_suspended: bool = True, skip_locked: bool = True, with_retries_left: bool = True,
                       process_id: int = None) -> List[ExternalTask]:
        body_params = {'active': skip_suspended, 'notLocked': skip_locked, "withRetriesLeft": with_retries_left}
        if process_id:
            body_params['processInstanceId'] = process_id
        processes_descriptions: List[dict] = await self.camunda.post('/external-task', body_params=body_params)

        external_tasks = [ExternalTask(
            id=processes_description["id"],
            activity_id=processes_description["activityId"],
            activity_instance_id=processes_description["activityInstanceId"],
            process_instance_id=processes_description["processInstanceId"],
            topic_name=processes_description["topicName"],
        ) for processes_description in processes_descriptions]
        return external_tasks

    async def get_id_to_task(self, skip_suspended: bool = True, skip_locked: bool = True,
                             with_retries_left: bool = True, process_id: int = None) -> Dict[str, ExternalTask]:
        external_tasks = await self.get_list(skip_suspended=skip_suspended, skip_locked=skip_locked,
                                             process_id=process_id, with_retries_left=with_retries_left)
        external_task_id_to_external_task = {task.id: task for task in external_tasks}
        return external_task_id_to_external_task

    async def lock(self, task_id: str, worker_id: str, lock_duration_ms: int) -> None:
        body_params = {'workerId': worker_id, 'lockDuration': lock_duration_ms}
        await self.camunda.post(f'/external-task/{task_id}/lock', body_params=body_params)

    async def bpmn_error(self, task_id: str, worker_id: str, error_message: str, error_code: str) -> None:
        body_params = {'workerId': worker_id, 'errorCode': error_code, "errorMessage": error_message}
        await self.camunda.post(f'/external-task/{task_id}/bpmnError', body_params=body_params)

    async def failure(self, task_id: str, worker_id: str, retry_timeout: int, retries: int, error_message: str) -> None:
        body_params = {'workerId': worker_id, 'retryTimeout': retry_timeout,
                       "errorMessage": error_message, "retries": retries}
        await self.camunda.post(f'/external-task/{task_id}/failure', body_params=body_params)

    async def complete(self, task_id: str, worker_id: str, variables: Dict[str, Any]) -> None:
        body_params = {'workerId': worker_id, 'variables': self.camunda.pack_variables(variables)}
        await self.camunda.post(f'/external-task/{task_id}/complete', body_params=body_params)
