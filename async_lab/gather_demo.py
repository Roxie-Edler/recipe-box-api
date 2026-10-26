
import asyncio
import time

async def sleeper(name, delay):
    await asyncio.sleep(delay)
    print(f"{name} done")
    return f"{name} done"


async def main():
    print("Starting gather demo...")

    task1 = asyncio.create_task(sleeper("first", 1))
    task2 = asyncio.create_task(sleeper("second", 2))
    task3 = asyncio.create_task(sleeper("third", 3))

    print("Created all three tasks!")

    start = time.perf_counter()
    results = await asyncio.gather(task1, task2, task3)
    end = time.perf_counter()
    elapsed = end - start

    print("Results:", results)
    print("Elapsed:", elapsed, "seconds")


if __name__ == "__main__":
    asyncio.run(main())
