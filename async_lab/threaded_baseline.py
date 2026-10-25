
import time
import httpx
import threading

url = "http://127.0.0.1:5001/nutrition/eggs"

def fetch_once():
    httpx.get(url)

for num_calls in [1, 3, 5]:
    threads = []

    start = time.perf_counter()

    for _ in range(num_calls):
        thread = threading.Thread(target=fetch_once)
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    end = time.perf_counter()

    print(f"{num_calls} threaded calls: {end - start:.6f} seconds")

