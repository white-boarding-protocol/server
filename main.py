from whiteboarding.whiteboarding import Whiteboarding
import asyncio


async def nested():
    print("here")
    return 42


async def main():
    # Schedule nested() to run soon concurrently
    # with "main()".
    task = asyncio.create_task(nested())

    # "task" can now be used to cancel "nested()", or
    # can simply be awaited to wait until it is complete:
    await asyncio.sleep(2)
    print("before")
    await task
    print(task.result())


if __name__ == "__main__":
    whiteboarding = Whiteboarding()
    asyncio.run(whiteboarding.start())
    # asyncio.run(main())
