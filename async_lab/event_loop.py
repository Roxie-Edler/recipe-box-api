
"""
Rule: A blocking call like time.sleep() freezes the event loop,
preventing all other coroutines sharing it from running until it finishes.
"""

import asyncio
import time


async def healthy_ping():
    print("healthy ping: start")
    await asyncio.sleep(1)
    print("healthy ping: end")


async def healthy_pong():
    print("healthy pong: start")
    await asyncio.sleep(0.2)
    print("healthy pong: end")


async def healthy_demo():
    print("\n=== Healthy version ===")
    await asyncio.gather(healthy_ping(), healthy_pong())
    print("healthy demo: complete")


async def stalled_ping():
    print("stalled ping: start")
    time.sleep(1)  # Blocks the event loop!
    print("stalled ping: end")


async def stalled_pong():
    print("stalled pong: start")
    await asyncio.sleep(0.2)
    print("stalled pong: end")


async def stalled_demo():
    print("\n=== Stalled version ===")
    await asyncio.gather(stalled_ping(), stalled_pong())
    print("stalled demo: complete")


async def main():
    await healthy_demo()
    await stalled_demo()


if __name__ == "__main__":
    asyncio.run(main())
