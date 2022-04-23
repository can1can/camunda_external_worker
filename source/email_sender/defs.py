#  Copyright (C) 2022
#  Moscow
#  PUBLISHED MATERIAL.
#
#  Authors: Vasiliev Ivan <open.source.can1can@gmail.com>
#
from enum import Enum


class EncryptionMethod(str, Enum):
    ssl = 'SSL'
    tls = 'TLS'


class Sender:
    def __init__(self, name: str, email: str, login: str, password: str, smtp_server: str, smtp_port: int,
                 encryption_method: str = EncryptionMethod.tls.value):
        self.name = name
        self.email = email
        self.login = login
        self.password = password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.encryption_method = encryption_method

    def __dict__(self):
        return {
                "name": self.name,
                "email_sender": self.email,
                "login": self.login,
                "smtp_server": self.smtp_server,
                "smtp_port": self.smtp_port,
                "encryption_method": self.encryption_method}

