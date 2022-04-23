#  Copyright (C) 2022
#  Moscow
#  PUBLISHED MATERIAL.
#
#  Authors: Vasiliev Ivan <open.source.can1can@gmail.com>
#
import logging

from connectors.camunda_connector.connector import CamundaConnector
from connectors.camunda_connector.defs import ExternalTask
from connectors.cat_fact_connector import CatFactConnector
from external_tasks.external_task_handler import AbstractExternalTaskHandler, ExternalTaskResult, \
    ExternalTaskSuccess

logger = logging.getLogger(__name__)


class CatFactHandler(AbstractExternalTaskHandler):
    class Context:
        camunda_connector: CamundaConnector = None
        cat_fact_connector: CatFactConnector = None

    async def _handle_task(self, camunda_task: ExternalTask, topic_args: dict) -> ExternalTaskResult:
        logger.debug(f"handling camunda task: {camunda_task} with args: {topic_args}")
        fact = await self.context.cat_fact_connector.get_fact()
        logger.info(f"fact: {fact}")
        return ExternalTaskSuccess(variables={"fact": fact})
    # @dataclass
    # class Context:
    #     base_camunda_connector: BaseCamundaConnector
    #     kafka_handler: KafkaHandler
    # def __init__(self, co):