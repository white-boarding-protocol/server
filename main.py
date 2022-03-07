from whiteboarding.exceptions import InvalidConfig
from whiteboarding.whiteboarding import Whiteboarding
import asyncio
import logging
import os

if __name__ == "__main__":
    # TODO check if the logging path exists

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(name)s :: %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S', filename='whiteboarding.log', filemode='a')
    try:
        whiteboarding = Whiteboarding()
        asyncio.run(whiteboarding.start())
    except InvalidConfig:
        pass
