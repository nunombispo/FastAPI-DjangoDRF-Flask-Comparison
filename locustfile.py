from locust import HttpUser, task, between
import random
import json

class APIUser(HttpUser):
    wait_time = between(1, 3)  # Wait 1-3 seconds between requests
    
    def on_start(self):
        """Initialize user data"""
        self.item_ids = []
        self.base_urls = {
            "fastapi": "http://localhost:8000",
            "flask": "http://localhost:5000", 
            "drf": "http://localhost:8001"
        }
        self.current_api = random.choice(list(self.base_urls.keys()))
        self.base_url = self.base_urls[self.current_api]
    
    @task(3)
    def list_items(self):
        """List all items - most common operation"""
        with self.client.get(f"{self.base_url}/items/", catch_response=True) as response:
            if response.status_code == 200:
                try:
                    items = response.json()
                    response.success()
                except json.JSONDecodeError:
                    response.failure("Invalid JSON response")
            else:
                response.failure(f"Failed with status {response.status_code}")
    
    @task(2)
    def create_item(self):
        """Create a new item"""
        item_data = {
            "name": f"Test Item {random.randint(1, 1000)}",
            "description": f"Description for item {random.randint(1, 1000)}",
            "price": round(random.uniform(10.0, 1000.0), 2),
            "in_stock": random.choice([True, False])
        }
        
        with self.client.post(f"{self.base_url}/items/", 
                             json=item_data, 
                             catch_response=True) as response:
            if response.status_code in [200, 201]:
                try:
                    result = response.json()
                    if "id" in result:
                        self.item_ids.append(result["id"])
                        response.success()
                    else:
                        response.failure("No ID in response")
                except json.JSONDecodeError:
                    response.failure("Invalid JSON response")
            else:
                response.failure(f"Failed with status {response.status_code}")
    
    @task(2)
    def get_item(self):
        """Get a specific item"""
        if not self.item_ids:
            return  # Skip if no items available
        
        item_id = random.choice(self.item_ids)
        
        # Handle DRF trailing slash requirement
        if self.current_api == "drf":
            url = f"{self.base_url}/items/{item_id}/"
        else:
            url = f"{self.base_url}/items/{item_id}"
        
        with self.client.get(url, catch_response=True) as response:
            if response.status_code == 200:
                try:
                    item = response.json()
                    if "id" in item:
                        response.success()
                    else:
                        response.failure("Invalid item response")
                except json.JSONDecodeError:
                    response.failure("Invalid JSON response")
            elif response.status_code == 404:
                # Item might have been deleted, remove from list
                if item_id in self.item_ids:
                    self.item_ids.remove(item_id)
                response.success()  # 404 is expected for deleted items
            else:
                response.failure(f"Failed with status {response.status_code}")
    
    @task(1)
    def update_item(self):
        """Update an existing item"""
        if not self.item_ids:
            return  # Skip if no items available
        
        item_id = random.choice(self.item_ids)
        update_data = {
            "name": f"Updated Item {random.randint(1, 1000)}",
            "description": f"Updated description {random.randint(1, 1000)}",
            "price": round(random.uniform(10.0, 1000.0), 2),
            "in_stock": random.choice([True, False])
        }
        
        # Handle DRF trailing slash requirement
        if self.current_api == "drf":
            url = f"{self.base_url}/items/{item_id}/"
        else:
            url = f"{self.base_url}/items/{item_id}"
        
        with self.client.put(url, 
                            json=update_data, 
                            catch_response=True) as response:
            if response.status_code == 200:
                try:
                    result = response.json()
                    if "id" in result:
                        response.success()
                    else:
                        response.failure("Invalid update response")
                except json.JSONDecodeError:
                    response.failure("Invalid JSON response")
            elif response.status_code == 404:
                # Item might have been deleted, remove from list
                if item_id in self.item_ids:
                    self.item_ids.remove(item_id)
                response.success()  # 404 is expected for deleted items
            else:
                response.failure(f"Failed with status {response.status_code}")
    
    @task(1)
    def delete_item(self):
        """Delete an item"""
        if not self.item_ids:
            return  # Skip if no items available
        
        item_id = random.choice(self.item_ids)
        
        # Handle DRF trailing slash requirement
        if self.current_api == "drf":
            url = f"{self.base_url}/items/{item_id}/"
        else:
            url = f"{self.base_url}/items/{item_id}"
        
        with self.client.delete(url, catch_response=True) as response:
            if response.status_code in [200, 204]:
                # Remove from our list
                if item_id in self.item_ids:
                    self.item_ids.remove(item_id)
                response.success()
            elif response.status_code == 404:
                # Item might have been deleted already, remove from list
                if item_id in self.item_ids:
                    self.item_ids.remove(item_id)
                response.success()  # 404 is expected for deleted items
            else:
                response.failure(f"Failed with status {response.status_code}")


class FastAPIUser(APIUser):
    """Dedicated user class for FastAPI testing"""
    
    def on_start(self):
        self.current_api = "fastapi"
        self.base_url = "http://localhost:8000"
        self.item_ids = []


class FlaskUser(APIUser):
    """Dedicated user class for Flask testing"""
    
    def on_start(self):
        self.current_api = "flask"
        self.base_url = "http://localhost:5000"
        self.item_ids = []


class DRFUser(APIUser):
    """Dedicated user class for Django REST Framework testing"""
    
    def on_start(self):
        self.current_api = "drf"
        self.base_url = "http://localhost:8001"
        self.item_ids = [] 