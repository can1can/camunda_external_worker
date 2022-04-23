#  Copyright (C) 2022
#  Moscow
#  PUBLISHED MATERIAL.
#
#  Authors: Mike Orlov <open.source.can1can@gmail.com>
#
from .base import BaseCamundaConnector
from .external_task import ExternalTaskConnector
from .process import ProcessConnector


class CamundaConnector:

    def __init__(self, server_address):
        base_connector = BaseCamundaConnector(server_address)
        self.process = ProcessConnector(base_connector)
        self.external_task = ExternalTaskConnector(base_connector)
