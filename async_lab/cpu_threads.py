
import time
import threading

def count():
    total = 0
    for i in range(50_000_000):
        total += 1
    return total

num_calls = 4

# Sequential execution
start = time.perf_counter()

for _ in range(num_calls):
    count()

end = time.perf_counter()
print(f"Sequential ({num_calls} runs): {end - start:.6f} seconds")

# Threaded execution
threads = []

start = time.perf_counter()

for _ in range(num_calls):
    thread = threading.Thread(target=count)
    threads.append(thread)

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

end = time.perf_counter()
print(f"Threaded ({num_calls} threads): {end - start:.6f} seconds")
