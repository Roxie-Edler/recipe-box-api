
import asyncio
import time
import httpx


async def main():
    start = time.perf_counter()

    async with httpx.AsyncClient() as client:
        await client.get("http://127.0.0.1:5001/nutrition/eggs")
        await client.get("http://127.0.0.1:5001/nutrition/eggs")
        await client.get("http://127.0.0.1:5001/nutrition/eggs")

    elapsed = time.perf_counter() - start
    print(f"Total time: {elapsed:.6f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
