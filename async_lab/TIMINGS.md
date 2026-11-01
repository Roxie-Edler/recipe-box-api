sync baseline against slow-service (127.0.0.1:5001)

1 call  to /nutrition/eggs: 1.042442 s
3 calls to /nutrition/eggs: 3.051676 s
5 calls to /nutrition/eggs: 5.070987 s

Measured with sync_baseline.py using httpx and time.perf_counter().


async sequential httpx, 3 calls: 3.064129 seconds
async gather httpx, 3 calls: 1.052505 seconds

With a 0.5s timeout, we give up the chance for slower requests to finish successfully in order to get predictable ~0.5s responses and avoid the script hanging for several seconds.