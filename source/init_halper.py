#  Copyright (C) 2022
#  Moscow
#  PUBLISHED MATERIAL.
#
#  Authors: Vasiliev Ivan <open.source.can1can@gmail.com>
#
"""functions, that must be called at server start-up"""
import argparse
import configparser
import logging
import sys
VERSION = "develop"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('-c', '--config', dest='config', type=get_config
                        )
    return parser.parse_args()


def get_config(path: str) -> dict:
    config = configparser.ConfigParser()
    config.read(path)
    return config.__dict__['_sections']


def init_logs(log_level: str) -> None:
    root = logging.getLogger()
    root.setLevel(logging.getLevelName(log_level))
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.getLevelName(log_level))
    formatter = logging.Formatter('%(asctime)s|%(version)s|%(name)s|%(levelname)s>- %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)
    old_factory = logging.getLogRecordFactory()
    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        record.version = VERSION
        return record
    logging.setLogRecordFactory(record_factory)
    logging.getLogger('asyncio').setLevel(logging.ERROR)


