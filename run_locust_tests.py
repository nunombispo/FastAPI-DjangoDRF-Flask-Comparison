#!/usr/bin/env python3
"""
Locust Load Testing Script

This script runs Locust load tests against all three APIs (FastAPI, Flask, DRF)
with different user loads and scenarios.
"""

import subprocess
import time
import os
import sys
from datetime import datetime

def run_locust_test(api_name, host, users, spawn_rate, run_time, output_file):
    """Run a Locust test for a specific API"""
    
    print(f"\n{'='*60}")
    print(f"Starting Locust test for {api_name.upper()}")
    print(f"Host: {host}")
    print(f"Users: {users}")
    print(f"Spawn Rate: {spawn_rate} users/second")
    print(f"Run Time: {run_time} seconds")
    print(f"{'='*60}")
    
    # Create output directory if it doesn't exist
    os.makedirs("locust_results", exist_ok=True)
    
    # Run Locust command
    cmd = [
        "locust",
        "--host", host,
        "--users", str(users),
        "--spawn-rate", str(spawn_rate),
        "--run-time", f"{run_time}s",
        "--headless",  # Run without web UI
        "--html", f"locust_results/{output_file}.html",
        "--csv", f"locust_results/{output_file}",
        "--locustfile", "locustfile.py"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=run_time + 60)
        
        if result.returncode == 0:
            print(f"✅ {api_name.upper()} test completed successfully")
            print(f"📊 Results saved to: locust_results/{output_file}")
        else:
            print(f"❌ {api_name.upper()} test failed")
            print(f"Error: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {api_name.upper()} test timed out")
    except Exception as e:
        print(f"❌ {api_name.upper()} test error: {e}")

def main():
    """Main function to run all Locust tests"""
    
    print("🚀 Starting Locust Load Testing Suite")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test configurations
    test_configs = [
        {
            "name": "FastAPI",
            "host": "http://localhost:8000",
            "users": 50,
            "spawn_rate": 5,
            "run_time": 60
        },
        {
            "name": "Flask", 
            "host": "http://localhost:5000",
            "users": 50,
            "spawn_rate": 5,
            "run_time": 60
        },
        {
            "name": "DRF",
            "host": "http://localhost:8001", 
            "users": 50,
            "spawn_rate": 5,
            "run_time": 60
        }
    ]
    
    # Check if applications are running
    print("\n🔍 Checking if applications are running...")
    for config in test_configs:
        try:
            import requests
            response = requests.get(f"{config['host']}/items/", timeout=5)
            if response.status_code == 200:
                print(f"✅ {config['name']} is running at {config['host']}")
            else:
                print(f"⚠️  {config['name']} responded with status {response.status_code}")
        except Exception as e:
            print(f"❌ {config['name']} is not accessible: {e}")
            print("Please start the applications with: docker-compose up -d")
            sys.exit(1)
    
    # Run tests
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    for config in test_configs:
        output_file = f"{config['name'].lower()}_load_test_{timestamp}"
        run_locust_test(
            config["name"],
            config["host"], 
            config["users"],
            config["spawn_rate"],
            config["run_time"],
            output_file
        )
        
        # Wait between tests
        time.sleep(5)
    
    print(f"\n🎉 All Locust tests completed!")
    print(f"📁 Results saved in: locust_results/")
    print(f"📊 Open HTML files in your browser to view detailed results")

if __name__ == "__main__":
    main() 