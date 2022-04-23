#  Copyright (C) 2022
#  Moscow
#  PUBLISHED MATERIAL.
#
#  Authors: Vasiliev Ivan <open.source.can1can@gmail.com>
#
import hashlib
from typing import Union


def get_md5(payload: Union[bytes, str]) -> str:
    m = hashlib.md5()
    m.update(payload)
    return m.hexdigest()


def get_sha512(payload: Union[bytes, str]) -> str:
    m = hashlib.sha512()
    m.update(payload)
    return m.hexdigest()
