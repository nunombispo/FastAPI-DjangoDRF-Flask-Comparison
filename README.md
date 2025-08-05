# FastAPI vs Django REST Framework vs Flask Comparison

A comprehensive comparison of three popular Python web frameworks: **FastAPI**, **Django REST Framework (DRF)**, and **Flask**. This project includes production-ready Docker configurations with separate PostgreSQL instances for each application, optimized database connection pools for high-load benchmarking, and a comprehensive benchmarking script to test CRUD operations across all three frameworks.

## 🏗️ Project Structure

```
FastAPI-DjangoDRF-Flask-Comparison/
├── api_benchmark.py          # High-performance benchmark script
├── locustfile.py             # Locust load testing scenarios
├── run_locust_tests.py       # Automated Locust test runner
├── requirements-locust.txt    # Locust dependencies
├── docker-compose.yml        # Docker Compose configuration
├── fastapi_app/             # FastAPI application
│   ├── Dockerfile           # Production Dockerfile
│   ├── requirements.txt     # Python dependencies
│   ├── main.py             # FastAPI application
│   ├── models.py           # SQLAlchemy models
│   └── database.py         # Optimized database configuration
├── flask_app/              # Flask application
│   ├── Dockerfile          # Production Dockerfile
│   ├── requirements.txt    # Python dependencies
│   ├── app.py             # Flask application
│   ├── models.py          # SQLAlchemy models
│   └── database.py        # Optimized database configuration
└── drf_app/               # Django REST Framework application
    ├── Dockerfile         # Production Dockerfile
    ├── requirements.txt   # Python dependencies
    ├── manage.py         # Django management script
    ├── django_app/       # Django project settings
    └── api/              # DRF API app
        ├── models.py     # Django models
        ├── serializers.py # DRF serializers
        ├── views.py      # DRF views
        └── urls.py       # URL routing
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)

### Running with Docker Compose

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd FastAPI-DjangoDRF-Flask-Comparison
   ```

2. **Start all services:**

   ```bash
   docker-compose up -d
   ```

3. **Run the benchmark:**
   ```bash
   python api_benchmark.py
   ```

### Manual Setup (Local Development)

1. **Set up virtual environments:**

   ```bash
   # FastAPI
   cd fastapi_app
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt

   # Flask
   cd ../flask_app
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

   # DRF
   cd ../drf_app
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Start the applications:**

   ```bash
   # FastAPI (Terminal 1)
   cd fastapi_app
   uvicorn main:app --host 0.0.0.0 --port 8000

   # Flask (Terminal 2)
   cd flask_app
   gunicorn --bind 0.0.0.0:5000 app:app

   # DRF (Terminal 3)
   cd drf_app
   python manage.py migrate
   gunicorn --bind 0.0.0.0:8001 django_app.wsgi:application
   ```

3. **Run the benchmark:**
   ```bash
   python api_benchmark.py
   ```

## 📊 API Endpoints

All three applications provide the same REST API endpoints:

| Method   | Endpoint      | Description            |
| -------- | ------------- | ---------------------- |
| `GET`    | `/items/`     | List all items         |
| `POST`   | `/items/`     | Create a new item      |
| `GET`    | `/items/{id}` | Get a specific item    |
| `PUT`    | `/items/{id}` | Update a specific item |
| `DELETE` | `/items/{id}` | Delete a specific item |

### Item Schema

```json
{
  "id": 1,
  "name": "Test Item",
  "description": "A performance benchmark item",
  "price": 99.99,
  "in_stock": true
}
```

## 🔧 Framework Configurations

### FastAPI

- **Server**: Uvicorn (ASGI)
- **Port**: 8000
- **ORM**: SQLAlchemy with optimized connection pool
- **Documentation**: Auto-generated at `/docs`
- **Features**: Async/await, automatic validation, OpenAPI

### Flask

- **Server**: Gunicorn (WSGI)
- **Port**: 5000
- **ORM**: SQLAlchemy with Flask-SQLAlchemy and optimized connection pool
- **Features**: Lightweight, flexible, minimal boilerplate

### Django REST Framework

- **Server**: Gunicorn (WSGI)
- **Port**: 8001
- **ORM**: Django ORM with optimized connection settings
- **Features**: Built-in admin, comprehensive ecosystem, ViewSets

## 📈 High-Performance Benchmarking

The `api_benchmark.py` script performs comprehensive CRUD operations testing with optimized settings for high-load scenarios:

- **Operations**: POST (create), GET (read), PUT (update), DELETE (delete)
- **Concurrency**: 20 concurrent requests
- **Requests per test**: 500 items per framework (configurable)
- **Connection Management**: Optimized connection pooling and limits
- **Metrics**: Duration, success rate, failures, requests per second (RPS)

### Benchmark Features

- **Connection Pool Optimization**: Prevents database connection exhaustion
- **Strategic Delays**: Allows database stabilization between operations
- **Error Handling**: Robust exception handling with detailed logging
- **Progress Tracking**: Real-time progress updates for each operation
- **Performance Metrics**: Comprehensive performance analysis

### Sample Output

```
2025-08-05 15:11:27,332 - INFO - Starting API Benchmark...
2025-08-05 15:11:27,333 - INFO - ==================================================
2025-08-05 15:11:27,335 - INFO - Testing FASTAPI at http://localhost:8000/items/
2025-08-05 15:11:27,336 - INFO - Starting benchmark for FASTAPI...
2025-08-05 15:11:27,337 - INFO - FASTAPI - Creating 500 items...
2025-08-05 15:11:27,338 - INFO - FASTAPI - Created 500 items
2025-08-05 15:11:27,339 - INFO - FASTAPI - Reading 500 items...
2025-08-05 15:11:27,340 - INFO - FASTAPI - Updating 500 items...
2025-08-05 15:11:27,341 - INFO - FASTAPI - Deleting 500 items...
2025-08-05 15:11:27,342 - INFO - FASTAPI - Benchmark completed
2025-08-05 15:11:27,343 - INFO - FASTAPI =>
2025-08-05 15:11:27,344 - INFO -   Duration: 2.46s
2025-08-05 15:11:27,345 - INFO -   Success: 2000/2000
2025-08-05 15:11:27,346 - INFO -   Failures: 0
2025-08-05 15:11:27,347 - INFO -   RPS: 813.01
```

## 🐛 Locust Load Testing

In addition to the custom benchmark script, this project includes comprehensive Locust load testing for realistic user scenarios.

### Features

- **Realistic User Behavior**: Simulates actual user interactions with random data
- **CRUD Operations**: Tests all Create, Read, Update, Delete operations
- **Multiple User Classes**: Dedicated test classes for each framework
- **Comprehensive Metrics**: Response times, failure rates, throughput
- **HTML Reports**: Detailed visual reports with charts and statistics
- **CSV Export**: Raw data export for further analysis

### Installation

```bash
# Install Locust
pip install -r requirements-locust.txt

# Or install directly
pip install locust==2.17.0
```

### Running Locust Tests

#### Quick Start

```bash
# Run automated test suite
python run_locust_tests.py
```

#### Manual Testing

```bash
# Start Locust web interface
locust --host http://localhost:8000 --locustfile locustfile.py

# Run headless test for FastAPI
locust --host http://localhost:8000 --users 50 --spawn-rate 5 --run-time 60s --headless --html results.html

# Run headless test for Flask
locust --host http://localhost:5000 --users 50 --spawn-rate 5 --run-time 60s --headless --html results.html

# Run headless test for DRF
locust --host http://localhost:8001 --users 50 --spawn-rate 5 --run-time 60s --headless --html results.html
```

### Test Scenarios

The Locust test suite includes:

#### **APIUser Class** (Mixed API Testing)

- **Random API Selection**: Tests all three APIs randomly
- **Realistic Workload**: 3:2:2:1 ratio for GET:POST:PUT:DELETE operations
- **Dynamic Data**: Random item names, prices, and descriptions
- **Error Handling**: Graceful handling of 404s and invalid responses

#### **Framework-Specific Classes**

- **FastAPIUser**: Dedicated FastAPI testing
- **FlaskUser**: Dedicated Flask testing
- **DRFUser**: Dedicated DRF testing

### Test Operations

| Operation       | Weight | Description                                |
| --------------- | ------ | ------------------------------------------ |
| **List Items**  | 3      | GET `/items/` - Most common operation      |
| **Create Item** | 2      | POST `/items/` - Add new items             |
| **Get Item**    | 2      | GET `/items/{id}` - Retrieve specific item |
| **Update Item** | 1      | PUT `/items/{id}` - Modify existing item   |
| **Delete Item** | 1      | DELETE `/items/{id}` - Remove item         |

### Sample Locust Output

```
🚀 Starting Locust Load Testing Suite
📅 2025-08-05 15:30:00

============================================================
Starting Locust test for FASTAPI
Host: http://localhost:8000
Users: 50
Spawn Rate: 5 users/second
Run Time: 60 seconds
============================================================

✅ FASTAPI test completed successfully
📊 Results saved to: locust_results/fastapi_load_test_20250805_153000
```

### Results Analysis

Locust generates comprehensive reports including:

- **Response Time Statistics**: Min, max, median, 95th percentile
- **Request Rate**: Requests per second
- **Failure Rate**: Percentage of failed requests
- **User Count**: Concurrent users over time
- **Response Time Distribution**: Histogram of response times

### Configuration

#### Test Parameters

```python
# run_locust_tests.py
test_configs = [
    {
        "name": "FastAPI",
        "host": "http://localhost:8000",
        "users": 50,           # Number of concurrent users
        "spawn_rate": 5,       # Users spawned per second
        "run_time": 60         # Test duration in seconds
    }
]
```

#### Custom Scenarios

```python
# locustfile.py
@task(3)  # Weight for this task
def list_items(self):
    # Custom test logic
    pass
```

### Advanced Usage

#### Stress Testing

```bash
# High load test
locust --host http://localhost:8000 --users 200 --spawn-rate 10 --run-time 300s --headless
```

#### Web Interface

```bash
# Start web UI for interactive testing
locust --host http://localhost:8000 --locustfile locustfile.py
# Then open http://localhost:8089
```

#### Custom User Classes

```python
# Test specific framework
class FastAPIUser(APIUser):
    def on_start(self):
        self.current_api = "fastapi"
        self.base_url = "http://localhost:8000"
```

## 🐳 Docker Configuration

### Database Architecture

Each API has its own dedicated PostgreSQL instance for complete isolation:

| Application | Database Container | Database Name    | External Port | Internal Port |
| ----------- | ------------------ | ---------------- | ------------- | ------------- |
| **FastAPI** | `pg-fastapi`       | `testdb_fastapi` | `5432`        | `5432`        |
| **Flask**   | `pg-flask`         | `testdb_flask`   | `5433`        | `5432`        |
| **DRF**     | `pg-drf`           | `testdb_drf`     | `5434`        | `5432`        |

### Benefits of Separate Databases

- **Complete Isolation**: Each application has its own database instance
- **Independent Scaling**: Each database can be scaled independently
- **No Shared Dependencies**: Issues with one database won't affect others
- **Better Performance**: No resource contention between applications
- **Easier Debugging**: Isolated issues and easier troubleshooting

### Database Connection Optimization

All applications use optimized database connection pools for high-load scenarios:

#### FastAPI & Flask (SQLAlchemy)

```python
# Connection pool settings
pool_size=20,           # Increased from default 5
max_overflow=30,        # Increased from default 10
pool_pre_ping=True,     # Verify connections before use
pool_recycle=3600,      # Recycle connections every hour
pool_timeout=60         # Increased timeout
```

#### Django (Django ORM)

```python
# Connection settings
MAX_CONNS=20,           # Maximum connections
CONN_MAX_AGE=600,       # Connection lifetime in seconds
conn_health_checks=True  # Health check connections
```

### Production-Ready Features

All Dockerfiles include:

- **Base Image**: Python 3.11-slim
- **Security**: Non-root user (`appuser`)
- **Performance**: Optimized layer caching
- **Health Checks**: Application-specific endpoints
- **Environment**: Production-ready settings
- **Database Waiting**: Applications wait for their respective databases to be ready
- **Connection Optimization**: High-performance database connection pools

### Docker Compose Services

- **postgres-fastapi**: PostgreSQL instance for FastAPI (port 5432)
- **postgres-flask**: PostgreSQL instance for Flask (port 5433)
- **postgres-drf**: PostgreSQL instance for DRF (port 5434)
- **fastapi**: FastAPI application on port 8000
- **flask**: Flask application on port 5000
- **drf**: Django REST Framework on port 8001

### Health Checks and Dependencies

Each application waits for its respective database to be healthy before starting:

```yaml
depends_on:
  postgres-fastapi:
    condition: service_healthy
```

This ensures proper startup order and prevents connection errors.

## 🔍 Key Differences

| Aspect              | FastAPI         | Flask      | Django REST Framework |
| ------------------- | --------------- | ---------- | --------------------- |
| **Learning Curve**  | Moderate        | Easy       | Steep                 |
| **Performance**     | Excellent       | Good       | Good                  |
| **Async Support**   | Native          | Limited    | Limited               |
| **Documentation**   | Auto-generated  | Manual     | Manual                |
| **Admin Interface** | None            | None       | Built-in              |
| **Validation**      | Pydantic        | Manual     | Serializers           |
| **URL Routing**     | Path parameters | Decorators | URL patterns          |
| **Connection Pool** | Optimized       | Optimized  | Optimized             |

## 🛠️ Development

### Adding New Features

1. **FastAPI**: Add endpoints in `fastapi_app/main.py`
2. **Flask**: Add routes in `flask_app/app.py`
3. **DRF**: Add views in `drf_app/api/views.py`

### Database Migrations

- **FastAPI/Flask**: SQLAlchemy handles migrations automatically
- **DRF**: Run `python manage.py makemigrations` and `python manage.py migrate`

### Testing

```bash
# Test individual applications
curl http://localhost:8000/items/  # FastAPI
curl http://localhost:5000/items/  # Flask
curl http://localhost:8001/items/  # DRF
```

### Database Access

```bash
# Connect to individual databases
psql -h localhost -p 5432 -U testuser -d testdb_fastapi  # FastAPI DB
psql -h localhost -p 5433 -U testuser -d testdb_flask    # Flask DB
psql -h localhost -p 5434 -U testuser -d testdb_drf      # DRF DB
```

### Performance Tuning

#### Benchmark Configuration

```python
# api_benchmark.py
NUM_REQUESTS = 500    # Number of items to create per framework
CONCURRENCY = 20      # Concurrent requests
```

#### Connection Pool Tuning

```python
# For higher load, increase these values:
pool_size=30,         # More base connections
max_overflow=50,      # More overflow connections
pool_timeout=120      # Longer timeout
```

## 📝 Logging

The benchmark script creates timestamped log files:

- **File**: `api_benchmark_YYYYMMDD_HHMMSS.log`
- **Console**: Real-time output
- **Level**: INFO and above
- **Format**: Timestamp, level, message
- **Progress**: Detailed operation progress tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- FastAPI team for the excellent async framework
- Flask team for the lightweight WSGI framework
- Django team for the comprehensive web framework
- SQLAlchemy team for the powerful ORM
