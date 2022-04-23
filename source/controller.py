#  Copyright (C) 2022
#  Moscow
#  PUBLISHED MATERIAL.
#
#  Authors: Vasiliev Ivan <open.source.can1can@gmail.com>
#
import logging
from dataclasses import dataclass
from typing import NoReturn

from connectors.camunda_connector.base import BaseCamundaConnector
from external_task_manager import ExternalTaskManager
from external_tasks.cat_fact_handler import CatFactHandler
from external_tasks.email_send_handler import EmailSendHandler
from external_tasks.random_image_handler import RandomImageHandler
from external_tasks.wotermark_handler import WaterMarkHandler

logger = logging.getLogger(__file__)


class Controller:
    @dataclass
    class Context:
        base_camunda_connector: BaseCamundaConnector = None
        external_task_manager: ExternalTaskManager = None

    def __init__(self, context, worker_id: str = "bmpn_course"):
        self.context = context
        self.worker_id = worker_id

    async def run(self) -> NoReturn:
        fact_handler = CatFactHandler(self.context, "get_fact", worker_id=self.worker_id, lock_duration = 3000)
        image_handler = RandomImageHandler(self.context, "get_image", worker_id=self.worker_id, lock_duration = 3000)
        watermark_handler = WaterMarkHandler(self.context, "wotermark", worker_id=self.worker_id, lock_duration = 3000)
        email_handler = EmailSendHandler(self.context, "send_email", worker_id=self.worker_id, lock_duration = 5000)
        self.context.external_task_manager.register_external_task_handler(fact_handler)
        self.context.external_task_manager.register_external_task_handler(image_handler)
        self.context.external_task_manager.register_external_task_handler(watermark_handler)
        self.context.external_task_manager.register_external_task_handler(email_handler)
        await self.context.external_task_manager.run_monitoring()

