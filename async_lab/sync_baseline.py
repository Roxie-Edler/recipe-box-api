import time
import httpx

url = "http://127.0.0.1:5001/nutrition/eggs"

for num_calls in [1, 3, 5]:
    start = time.perf_counter()

    for _ in range(num_calls):
        httpx.get(url)

    end = time.perf_counter()
    print(f"{num_calls} call(s): {end - start:.6f} seconds")