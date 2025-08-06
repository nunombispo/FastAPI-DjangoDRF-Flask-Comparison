# FastAPI vs Django REST Framework vs Flask Comparison

A comprehensive comparison of three popular Python web frameworks: **FastAPI**, **Django REST Framework (DRF)**, and **Flask**. This project includes production-ready Docker configurations with separate PostgreSQL instances for each application, optimized database connection pools for high-load benchmarking, comprehensive Locust load testing, and a benchmarking script to test CRUD operations across all three frameworks.

If this script was useful to you, consider donating to support the Developer Service Blog: https://buy.stripe.com/bIYdTrggi5lZamkdQW

## 🏗️ Project Structure

```
FastAPI-DjangoDRF-Flask-Comparison/
├── api_benchmark.py          # High-performance benchmark script
├── locustfile.py             # Locust load testing scenarios
├── run_locust_tests.py       # Automated Locust test runner
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
   git clone https://github.com/nunombispo/FastAPI-DjangoDRF-Flask-Comparison
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

4. **Run Locust load tests:**
   ```bash
   python run_locust_tests.py
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

### Running Locust Tests

#### Quick Start

```bash
# Run automated test suite
python run_locust_tests.py
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
