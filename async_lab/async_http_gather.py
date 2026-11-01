
import asyncio
import time
import httpx


async def main():
    url = "http://127.0.0.1:5001/nutrition/eggs"

    start = time.perf_counter()

    async with httpx.AsyncClient() as client:
        task1 = client.get(url)
        task2 = client.get(url)
        task3 = client.get(url)

        responses = await asyncio.gather(task1, task2, task3)

    elapsed = time.perf_counter() - start

    print(f"3 concurrent async call(s): {elapsed:.6f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
