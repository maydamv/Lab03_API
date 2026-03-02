import httpx
import csv
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from ratelimit import limits, sleep_and_retry

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

URL = "http://127.0.0.1:8000/item" 

@sleep_and_retry
@limits(calls=18, period=1)
def fetch_order(item_id):
    attempts = 0
    while attempts < 5:
        try:
            with httpx.Client(timeout=2.0) as client:
                response = client.get(f"{URL}/{item_id}")
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        'order_id': data['order_id'],
                        'account_id': data['account_id'],
                        'company': data['company'],
                        'status': data['status'],
                        'currency': data['currency'],
                        'subtotal': data['subtotal'],
                        'tax': data['tax'],
                        'total': data['total'],
                        'created_at': data['created_at']
                    }
                
                if response.status_code == 429:
                    wait = int(response.headers.get("Retry-After", 1))
                    logger.warning(f"ID {item_id}: 429 Limit. Waiting {wait}s...")
                    time.sleep(wait)
                elif response.status_code >= 500:
                    logger.warning(f"ID {item_id}: Error {response.status_code}. Retrying...")
                    time.sleep(1)
                else:
                    logger.error(f"ID {item_id}: Error fatal {response.status_code}")
                    break
        except Exception as e:
            logger.warning(f"ID {item_id}: Conexion error/timeout. Retrying...")
            time.sleep(1)
        attempts += 1
    return None

def main():
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(fetch_order, range(1, 1001)))
    
    valid_data = [r for r in results if r]
    
    fields = ['order_id', 'account_id', 'company', 'status', 'currency', 'subtotal', 'tax', 'total', 'created_at']
    with open('items_threads.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(valid_data)
    
    logger.info(f"Completed: {len(valid_data)} rows saved.")

if __name__ == "__main__":
    main()

