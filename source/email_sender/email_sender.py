#  Copyright (C) 2022
#  Moscow
#  PUBLISHED MATERIAL.
#
#  Authors: Vasiliev Ivan <open.source.can1can@gmail.com>
#
import logging
from typing import List, Optional

from email_sender.defs import Sender, EncryptionMethod
import smtplib
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.header import Header
from typing import Union, List, Dict, Any

from file_handler import FileHandler


logger = logging.getLogger(__name__)


class EmailSender:
    class Context:
        file_handler: FileHandler = None

    def __init__(self,  context: Context, send_config: dict):
        self.context = context
        self.sender = Sender(
            name=send_config["name"],
            email=send_config["email"],
            login=send_config["login"],
            password=send_config["password"],
            smtp_server=send_config["smtp_server"],
            smtp_port=send_config["smtp_port"],
        )

    @staticmethod
    def form_html_message(data: str):
        return MIMEText(data, 'html', 'utf-8')

    async def generate_mail_attachment(self, file_id: str):
        content_type = "jpeg"
        result = MIMEBase('application', "octet-stream")
        content = await self.context.file_handler.load(file_id)
        result.set_payload(content)
        encoders.encode_base64(result)
        result.add_header('Content-Disposition', 'attachment; filename="' + file_id + f'.{content_type}"')
        return result

    async def send_email(self, addresses: List[str], subject: str, message_html: str,
                         file_id: Optional[Union[str, int]] = None, mailing_references: Optional[str] = None):
        logger.info(f"sending email to {addresses}")
        msg = MIMEMultipart('html')
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = '{} <{}>'.format(self.sender.name, self.sender.email)
        msg['To'] = ", ".join(addresses)
        if mailing_references:
            msg['References'] = mailing_references

        msg.attach(self.form_html_message(data=message_html))
        if file_id:
            msg.attach(await self.generate_mail_attachment(file_id=file_id))

        if self.sender.encryption_method == EncryptionMethod.ssl.value:
            # TODO add aiosmtplib
            mail = smtplib.SMTP_SSL(self.sender.smtp_server, self.sender.smtp_port)
            # mail.set_debuglevel(1)
            mail.ehlo()
            mail.login(self.sender.login, self.sender.password)
        else:  # self.sender.encryption_method == EncryptionMethod.tls.value:
            mail = smtplib.SMTP(self.sender.smtp_server, self.sender.smtp_port)
            # mail.set_debuglevel(1)
            mail.ehlo()
            mail.starttls()
            mail.ehlo()
            mail.login(self.sender.login, self.sender.password)

        try:
            mail.sendmail(self.sender.email, msg["To"].split(","), msg.as_string())
        except smtplib.SMTPException as er:
            raise er
        finally:
            mail.quit()
        logger.info(f" email sent {addresses}")

