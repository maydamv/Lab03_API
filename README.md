# Lab 03 - API Client con Threads

This project implements a multithreaded synchronous client to consume a rate-limited API.

## Features
- Uses `ThreadPoolExecutor` with 10 threads.

- Rate limit of 18 requests per second to prevent server crashes.

- Handles 429 errors (Rate Limit) using the `Retry-After` header.

- Handles 5xx errors with automatic retries after 1 second.

- Generates a CSV file containing 1000 processed records.

