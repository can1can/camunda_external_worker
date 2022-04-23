#  Copyright (C) 2022
#  Moscow
#  PUBLISHED MATERIAL.
#
#  Authors: Vasiliev Ivan <open.source.can1can@gmail.com>
#
import asyncio
import logging


from initer import Initer

logger = logging.getLogger(__file__)
logger.info("APP STARTED")
initer = Initer()


async def amain():
    async with initer as controller:
        await controller.run()
    logger.info("EXITING")


asyncio.run(amain())
