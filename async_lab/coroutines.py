
import asyncio
import time

async def ping():
    print("ping: start")
    #await asyncio.sleep(1)
    time.sleep(1)
    print("ping: end")

async def pong():
    print("pong: start")
    await asyncio.sleep(1)
    print("pong: end")

async def main():
    print("main: start")
    await asyncio.gather(ping(), pong())
    print("main: end")

asyncio.run(main())
