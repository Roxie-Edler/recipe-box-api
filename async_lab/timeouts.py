
import sys
import asyncio
from pathlib import Path
import httpx

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import Config # type: ignore


async def fetch_item(path: str, label: str):
    url = f"{Config.SLOW_SERVICE_URL}{path}"

    async with httpx.AsyncClient() as client:
        try:
            response = await asyncio.wait_for(
                client.get(url),
                timeout=0.5
            )

            response.raise_for_status()

            return {
                "item": label,
                "status": "success",
                "url": url,
                "http_status": response.status_code
            }

        except asyncio.TimeoutError:
            return {
                "item": label,
                "status": "timed_out",
                "url": url
            }
        
        except httpx.ConnectError:
            return {
                "item": label, 
                "status": "connection_error",
                "url": url
            }


async def fetch_all():
    results = await asyncio.gather(
        fetch_item("/nutrition/eggs", "eggs"),
        fetch_item("/nutrition/bread", "bread"),
        fetch_item("/nutrition/tomatoes", "tomatoes")
    )

    return results


def main():
    results = asyncio.run(fetch_all())

    for result in results:
        print(result)


if __name__ == "__main__":
    main()

