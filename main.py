from whiteboarding.exceptions import InvalidConfig
from whiteboarding.whiteboarding import Whiteboarding
import asyncio
import logging

if __name__ == "__main__":
    data = {
        "user_id": "123",
        "type": 2,
        "action": 2,
        "event_type": 1,
        "target_user": "13",
        "message": "create_room",
    }

    # TODO check if the logging path exists

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(name)s :: %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S', filename='whiteboarding.log', filemode='a')
    try:
        whiteboarding = Whiteboarding()
        asyncio.run(whiteboarding.start())
    except InvalidConfig:
        pass
