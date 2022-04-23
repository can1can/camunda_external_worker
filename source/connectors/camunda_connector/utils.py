#  Copyright (C) 2022
#  Moscow
#  PUBLISHED MATERIAL.
#
#  Authors: Mike Orlov <open.source.can1can@gmail.com>
#
import datetime
from typing import Union


def to_java_bool_str(value: bool) -> str:
    return 'true' if value else 'false'


def to_java_datetime_str(value: datetime.datetime) -> str:
    datetime_str = value.isoformat(sep='T', timespec='milliseconds')
    if datetime_str[-3] == ':':
        datetime_str = datetime_str[:-3] + datetime_str[-2:]
    return datetime_str


def to_java_date_str(value: datetime.date) -> str:
    return f'{value.day}/{value.month}/{value.year}'


def to_java_str(value: Union[list, dict, int, float, bool, None, datetime.datetime]):
    if isinstance(value, bool):
        value = to_java_bool_str(value)
    if isinstance(value, datetime.datetime):
        value = to_java_datetime_str(value)
    return value


