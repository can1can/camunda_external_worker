#  Copyright (C) 2022
#  Moscow
#  PUBLISHED MATERIAL.
#
#  Authors: Vasiliev Ivan <open.source.can1can@gmail.com>
#
from abc import ABC, abstractmethod


class FileStorage(ABC):
    @abstractmethod
    async def save(self, **kwargs):
        pass

    @abstractmethod
    async def load(self, **kwargs):
        pass

    @abstractmethod
    async def delete(self, **kwargs):
        pass


class FileAlreadyExists(Exception):
    pass


class PathDoesNotExists(Exception):
    pass


class InsecurePath(Exception):
    pass
