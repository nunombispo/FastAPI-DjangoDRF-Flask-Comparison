import asyncio
import httpx
import time
import logging
from datetime import datetime

ENDPOINTS = {
    "fastapi": "http://localhost:8000/items/",
    "flask": "http://localhost:5000/items/",
    "drf": "http://localhost:8001/items/",
}

NUM_REQUESTS = 500
CONCURRENCY = 20

item_payload = {
    "name": "Test Item",
    "description": "A performance benchmark item",
    "price": 99.99,
    "in_stock": True
}

# Setup logging
def setup_logging():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"api_benchmark_{timestamp}.log"
    
    # Disable httpx logging
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, mode='w'),
            logging.StreamHandler()  # Also print to console
        ]
    )
    return log_filename

def print_metrics(name, duration, success, failures, total_requests):
    rps = success / duration if duration > 0 else 0
    logging.info(f"{name.upper()} =>")
    logging.info(f"  Duration: {duration:.2f}s")
    logging.info(f"  Success: {success}/{total_requests}")
    logging.info(f"  Failures: {failures}")
    logging.info(f"  RPS: {rps:.2f}")
    logging.info("")

async def post_item(client, url):
    try:
        r = await client.post(url, json=item_payload)
        
        if r.status_code in (200, 201):
            response_data = r.json()
            item_id = response_data.get("id")
            if item_id is None:
                # Try to find id in different possible formats
                if isinstance(response_data, dict):
                    for key, value in response_data.items():
                        if key.lower() == 'id' or (isinstance(value, int) and value > 0):
                            item_id = value
                            break
            return item_id
        else:
            logging.error(f"POST {url} - Failed with status {r.status_code}: {r.text}")
    except Exception as e:
        logging.error(f"POST {url} - Exception: {e}")
    return None

async def get_item(client, url, item_id):
    try:
        # Handle DRF trailing slash requirement
        if 'drf' in url or '8001' in url:
            get_url = f"{url}{item_id}/"
        else:
            get_url = f"{url}{item_id}"
        r = await client.get(get_url)
        if r.status_code == 200:
            return True
        else:
            logging.error(f"GET {get_url} - Failed: {r.text}")
            return False
    except Exception as e:
        logging.error(f"GET {url}{item_id} - Exception: {e}")
        return False

async def put_item(client, url, item_id):
    try:
        # Handle DRF trailing slash requirement
        if 'drf' in url or '8001' in url:
            put_url = f"{url}{item_id}/"
        else:
            put_url = f"{url}{item_id}"
        put_payload = {"name": "Updated", **item_payload}
        r = await client.put(put_url, json=put_payload)
        if r.status_code == 200:
            return True
        else:
            logging.error(f"PUT {put_url} - Failed: {r.text}")
            return False
    except Exception as e:
        logging.error(f"PUT {url}{item_id} - Exception: {e}")
        return False

async def delete_item(client, url, item_id):
    try:
        # Handle DRF trailing slash requirement
        if 'drf' in url or '8001' in url:
            delete_url = f"{url}{item_id}/"
        else:
            delete_url = f"{url}{item_id}"
        r = await client.delete(delete_url)
        if r.status_code in (200, 204):
            return True
        else:
            logging.error(f"DELETE {delete_url} - Failed: {r.text}")
            return False
    except Exception as e:
        logging.error(f"DELETE {url}{item_id} - Exception: {e}")
        return False

async def benchmark_crud(name, url):
    success = 0
    failures = 0
    item_ids = []

    logging.info(f"Starting benchmark for {name.upper()}...")
    
    # Use connection pooling and limits to prevent overwhelming the database
    limits = httpx.Limits(max_keepalive_connections=20, max_connections=50)
    timeout = httpx.Timeout(30.0, connect=10.0)
    
    async with httpx.AsyncClient(timeout=timeout, limits=limits) as client:
        start = time.perf_counter()

        # POST - Create items in batches to reduce connection pressure
        logging.info(f"{name.upper()} - Creating {NUM_REQUESTS} items...")
        post_tasks = [post_item(client, url) for _ in range(NUM_REQUESTS)]
        post_results = await asyncio.gather(*post_tasks, return_exceptions=True)
        item_ids.extend([id for id in post_results if id and not isinstance(id, Exception)])
        logging.info(f"{name.upper()} - Created {len(item_ids)} items")

        # Small delay to allow database to stabilize
        await asyncio.sleep(1)

        # GET - Read items
        logging.info(f"{name.upper()} - Reading {len(item_ids)} items...")
        get_tasks = [get_item(client, url, id) for id in item_ids]
        get_results = await asyncio.gather(*get_tasks, return_exceptions=True)

        # Small delay to allow database to stabilize
        await asyncio.sleep(1)

        # PUT - Update items
        logging.info(f"{name.upper()} - Updating {len(item_ids)} items...")
        put_tasks = [put_item(client, url, id) for id in item_ids]
        put_results = await asyncio.gather(*put_tasks, return_exceptions=True)

        # Small delay to allow database to stabilize
        await asyncio.sleep(1)

        # DELETE - Delete items
        logging.info(f"{name.upper()} - Deleting {len(item_ids)} items...")
        delete_tasks = [delete_item(client, url, id) for id in item_ids]
        delete_results = await asyncio.gather(*delete_tasks, return_exceptions=True)

        duration = time.perf_counter() - start

        total_requests = NUM_REQUESTS * 4  # POST + GET + PUT + DELETE
        success = sum([
            len([r for r in post_results if r and not isinstance(r, Exception)]),
            sum([r for r in get_results if r and not isinstance(r, Exception)]),
            sum([r for r in put_results if r and not isinstance(r, Exception)]),
            sum([r for r in delete_results if r and not isinstance(r, Exception)])
        ])
        failures = total_requests - success

        logging.info(f"{name.upper()} - Benchmark completed")
        print_metrics(name, duration, success, failures, total_requests)


async def main():
    # Setup logging
    log_filename = setup_logging()
    logging.info(f"Logging to: {log_filename}")
    
    logging.info("Starting API Benchmark...")
    logging.info("=" * 50)
    
    for name, url in ENDPOINTS.items():
        logging.info(f"Testing {name.upper()} at {url}")
        await benchmark_crud(name, url)
        # Add delay between frameworks to allow database recovery
        await asyncio.sleep(2)
    
    logging.info("Benchmark completed!")
    logging.info(f"Full log saved to: {log_filename}")

if __name__ == '__main__':
    asyncio.run(main())
