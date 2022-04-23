#  Copyright (C) 2022
#  Moscow
#  PUBLISHED MATERIAL.
#
#  Authors: Vasiliev Ivan <open.source.can1can@gmail.com>
#
from typing import Union

from filre_storage.file_storage import FileStorage


class FileHandler:
    # @dataclass
    # class Context:
    #     file_storage: FileStorage

    def __init__(self, file_storage: FileStorage):
        self.file_storage = file_storage

    async def upload(self, file: bytes) -> Union[int, str]:
        file_id = await self.file_storage.save(content=file)
        return file_id

    async def load(self, file_id: Union[int, str]):
        content = await self.file_storage.load(file_id=file_id)
        return content

    async def delete(self,  file_id: Union[int, str]):
        await self.file_storage.delete(file_id=file_id)
        return True
