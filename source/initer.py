#  Copyright (C) 2022
#  Moscow
#  PUBLISHED MATERIAL.
#
#  Authors: Vasiliev Ivan <open.source.can1can@gmail.com>
#
import logging
from dataclasses import dataclass

from aiohttp import ClientSession

from connectors.camunda_connector.connector import CamundaConnector
from connectors.cat_fact_connector import CatFactConnector
# from connectors.email_server_connector import EmailServerConnector
from connectors.rand_image_connector import RandomImageConnector
from controller import Controller
from email_sender.email_sender import EmailSender
from external_task_manager import ExternalTaskManager
from file_handler import FileHandler
from filre_storage.file_storage import FileStorage
from filre_storage.in_memory_storage import InMemoryStorage
from init_halper import parse_args, init_logs

logger = logging.getLogger(__name__)


@dataclass
class Initer:
    @dataclass
    class Context:
        session: ClientSession = None
        camunda_connector: CamundaConnector = None
        image_connector: RandomImageConnector = None
        # image_saver: CamundaConnector = None
        cat_fact_connector: CatFactConnector = None
        # email_server_connector: EmailServerConnector = None
        external_task_manager: ExternalTaskManager = None
        # file_storage: FileStorage = None
        file_handler: FileHandler = None
        email_sender: EmailSender = None

    context: Context
    config: dict

    def __init__(self):
        self.config = parse_args().config
        logging_settings = self.config.get('logging', {})
        log_level = logging_settings.get('level', 'INFO')
        init_logs(log_level)
        logger = logging.getLogger(__name__)
        logger.info(f'init with config; {self.config}')
        logging.getLogger('aiokafka').setLevel(logging.WARNING)

        self.context = self.Context()
        self.controller = None

    async def __aenter__(self) -> Controller:
        self.context.session = ClientSession()
        self.context.camunda_connector = CamundaConnector(self.config["camunda_connector"]["location"])
        self.context.image_connector = RandomImageConnector(self.config["image_getter"]["location"])
        self.context.cat_fact_connector = CatFactConnector(self.config["cat_fact"]["location"])
        self.context.external_task_manager = ExternalTaskManager(self.context)
        file_storage = InMemoryStorage()
        self.context.file_handler = FileHandler(file_storage)
        self.context.email_sender = EmailSender(self.context, self.config["email_sender"])
        self.controller = Controller(self.context)

        logger.debug(f"controller: {self.controller}")
        logger.info(f"----===== Init done ====----")
        return self.controller

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass



