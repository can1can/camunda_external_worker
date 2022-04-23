# -*- coding: utf-8 -*-
#  Copyright (C) 2022
#  Moscow
#  PUBLISHED MATERIAL.
#
#  Authors: Vasiliev Ivan <open.source.can1can@gmail.com>
#
import logging

from filre_storage.file_storage import FileStorage, FileAlreadyExists, PathDoesNotExists
from utils.hashes import get_md5, get_sha512

logger = logging.getLogger(__name__)


class InMemoryStorage(FileStorage):

    def __init__(self):
        self.__id_to_content = {}

    @staticmethod
    def __get_file_id(content: bytes) -> str:
        return get_md5(content)[:3] + "_" + get_sha512(content)[:3]

    async def save(self, content: bytes) -> str:
        file_id = self.__get_file_id(content)
        if file_id in self.__id_to_content:
            raise FileAlreadyExists()
        self.__id_to_content[file_id] = content
        return file_id

    async def rewrite(self, file_id: str, content: bytes):
        if file_id not in self.__id_to_content:
            raise PathDoesNotExists()
        self.__id_to_content[file_id] = content

    async def load(self, file_id: str) -> bytes:
        if file_id not in self.__id_to_content:
            raise PathDoesNotExists()
        content = self.__id_to_content[file_id]
        return content

    async def delete(self, file_id: str) -> None:
        if file_id not in self.__id_to_content:
            raise PathDoesNotExists()
        del self.__id_to_content[file_id]

