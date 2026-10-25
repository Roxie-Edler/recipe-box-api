
import asyncio

async def fetch_data():
    print("inside fetch_data")
    return 42

async def process_data():
    print("start process_data")
    value = await fetch_data()
    print("got from fetch_data:", value)
    return value * 2

async def main():
    final = await process_data()
    print("in main, final =", final)

asyncio.run(main())
