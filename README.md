# FastAPI vs Django REST Framework vs Flask Comparison

A comprehensive comparison of three popular Python web frameworks: **FastAPI**, **Django REST Framework (DRF)**, and **Flask**. This project includes production-ready Docker configurations and a benchmarking script to test CRUD operations across all three frameworks.

## 🏗️ Project Structure

```
FastAPI-DjangoDRF-Flask-Comparison/
├── api_benchmark.py          # Benchmark script for performance testing
├── docker-compose.yml        # Docker Compose configuration
├── fastapi_app/             # FastAPI application
│   ├── Dockerfile           # Production Dockerfile
│   ├── requirements.txt     # Python dependencies
│   ├── main.py             # FastAPI application
│   ├── models.py           # SQLAlchemy models
│   └── database.py         # Database configuration
├── flask_app/              # Flask application
│   ├── Dockerfile          # Production Dockerfile
│   ├── requirements.txt    # Python dependencies
│   ├── app.py             # Flask application
│   ├── models.py          # SQLAlchemy models
│   └── database.py        # Database configuration
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
- **ORM**: SQLAlchemy
- **Documentation**: Auto-generated at `/docs`
- **Features**: Async/await, automatic validation, OpenAPI

### Flask

- **Server**: Gunicorn (WSGI)
- **Port**: 5000
- **ORM**: SQLAlchemy with Flask-SQLAlchemy
- **Features**: Lightweight, flexible, minimal boilerplate

### Django REST Framework

- **Server**: Gunicorn (WSGI)
- **Port**: 8001
- **ORM**: Django ORM
- **Features**: Built-in admin, comprehensive ecosystem, ViewSets

## 📈 Benchmarking

The `api_benchmark.py` script performs comprehensive CRUD operations testing:

- **Operations**: POST (create), GET (read), PUT (update), DELETE (delete)
- **Concurrency**: 20 concurrent requests
- **Requests per test**: 5 items per framework
- **Metrics**: Duration, success rate, failures, requests per second (RPS)

### Sample Output

```
2025-08-05 15:11:27,332 - INFO - Starting API Benchmark...
2025-08-05 15:11:27,333 - INFO - ==================================================
2025-08-05 15:11:27,335 - INFO - Testing FASTAPI at http://localhost:8000/items/
2025-08-05 15:11:27,336 - INFO - Starting benchmark for FASTAPI...
2025-08-05 15:11:27,337 - INFO - FASTAPI - Created 5 items
2025-08-05 15:11:27,338 - INFO - FASTAPI - Benchmark completed
2025-08-05 15:11:27,339 - INFO - FASTAPI =>
2025-08-05 15:11:27,340 - INFO -   Duration: 0.46s
2025-08-05 15:11:27,341 - INFO -   Success: 20/20
2025-08-05 15:11:27,342 - INFO -   Failures: 0
2025-08-05 15:11:27,343 - INFO -   RPS: 43.15
```

## 🐳 Docker Configuration

### Production-Ready Features

All Dockerfiles include:

- **Base Image**: Python 3.11-slim
- **Security**: Non-root user (`appuser`)
- **Performance**: Optimized layer caching
- **Health Checks**: Application-specific endpoints
- **Environment**: Production-ready settings

### Docker Compose Services

- **fastapi**: FastAPI application on port 8000
- **flask**: Flask application on port 5000
- **drf**: Django REST Framework on port 8001
- **postgres**: PostgreSQL database (shared)

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

## 📝 Logging

The benchmark script creates timestamped log files:

- **File**: `api_benchmark_YYYYMMDD_HHMMSS.log`
- **Console**: Real-time output
- **Level**: INFO and above
- **Format**: Timestamp, level, message

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
