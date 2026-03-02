# Lab 03 - API Client con Threads

This project implements a multithreaded synchronous client to consume a rate-limited API.

## Features
- **Concurrency**: Uses `ThreadPoolExecutor` with 10 workers for efficient data fetching.
- **Rate Limiting**: Implemented a limit of 18 requests per second using the `ratelimit` library to stay below the server's 20 req/s threshold.
- **Resilience**: 
    - Handles **429 Too Many Requests**: Reads the `Retry-After` header and pauses execution.
    - Handles **5xx Internal Server Error**: Automatically retries after a 1-second delay.
    - **Timeouts**: Uses a 2.0s timeout per request to prevent hanging.
- **Data Export**: Generates `items_threads.csv` with 1000 records, filtering only the required fields (order_id, account_id, company, status, currency, subtotal, tax, total, created_at).

## Setup
1. Install dependencies: `uv pip install httpx ratelimit`
2. Run the server in one terminal: `orders_server`
3. Run the client: `python client_threads.py`

<img width="908" height="351" alt="imagen" src="https://github.com/user-attachments/assets/8ebf3672-da8f-427e-ab0e-4ad7324805c0" />


