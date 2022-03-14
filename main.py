from whiteboarding.exceptions import InvalidConfig
from whiteboarding.whiteboarding import Whiteboarding
import asyncio

if __name__ == "__main__":
    try:
        whiteboarding = Whiteboarding()
        asyncio.run(whiteboarding.start())
    except InvalidConfig:
        pass
