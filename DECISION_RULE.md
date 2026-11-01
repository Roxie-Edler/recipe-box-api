Why Async Fits This Workload

This endpoint makes three independent HTTP calls to a slow external service. The work is I/O-bound, and the calls don't depend on each other, so an async view can overlap their waiting time.

Using asyncio.gather(), the three approximately one-second calls can complete in about one second instead of three when the service is healthy.

Why Not Synchronous?

A synchronous view must wait for each call to finish before starting the next one. This means total response time is roughly the sum of all three calls.

My measurements showed approximately 3 seconds for the sequential version compared with approximately 1 second for the async version under the same conditions.

Why Not Threads?

Threads could also overlap I/O, but they introduce additional complexity and thread-management overhead.

Flask's async support and httpx.AsyncClient already provide I/O concurrency through an event loop, making async a straightforward fit for this endpoint.

Conclusion

Async is the right choice for this particular endpoint because it makes multiple independent network requests concurrently, reduces waiting time, and provides individual timeout and fallback handling when the external service is unavailable.