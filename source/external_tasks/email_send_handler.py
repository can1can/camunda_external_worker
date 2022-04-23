#  Copyright (C) 2022
#  Moscow
#  PUBLISHED MATERIAL.
#
#  Authors: Vasiliev Ivan <open.source.can1can@gmail.com>
#
import logging

from connectors.camunda_connector.defs import ExternalTask
from email_sender.email_sender import EmailSender
from external_tasks.external_task_handler import AbstractExternalTaskHandler, ExternalTaskResult, ExternalTaskSuccess
from file_handler import FileHandler

logger = logging.getLogger(__name__)


class EmailSendHandler(AbstractExternalTaskHandler):
    class Context:
        email_sender: EmailSender = None
        file_handler: FileHandler = None


    async def _handle_task(self, camunda_task: ExternalTask, topic_args: dict) -> ExternalTaskResult:
            logger.info(f"handling camunda task: {camunda_task} with args: {topic_args}")
            file_id = topic_args.get("file_id")
            send_to = topic_args.get("email")
            fact = topic_args.get("fact")
            # if not send_to:
            #     return 1
            await self.context.email_sender.send_email(addresses=[send_to], file_id=file_id,
                                                       subject="fact with image", message_html=fact)
            await self.context.file_handler.delete(file_id)
            # file_content = await self.context.file_storage.load(image_id)
            # logger.info(f"file_content: {file_content}")
            return ExternalTaskSuccess()
