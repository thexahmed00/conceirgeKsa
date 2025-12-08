# AJLA Concierge Platform

Python backend for AJLA - Premium Lifestyle Concierge Platform

## Project Setup

### Prerequisites
- Python 3.9+
- MySQL 8.0+
- Virtual environment

### Installation

1. **Create and activate virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables:**
```bash
cp .env.example .env
# Edit .env with your database credentials and JWT secret
```

4. **Initialize database:**
```bash
# Create MySQL database
mysql -u root -p
CREATE DATABASE ajla_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Running the Application

```bash
python main.py
```

The API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### Project Structure

```
/src
  /domain              # Domain entities, value objects, aggregates (DDD)
  /application         # Use cases, DTOs, orchestration layer
  /infrastructure      # Database, web layer, authentication
  /shared              # Shared utilities, exceptions, logging
/tests                 # Unit and integration tests
/main.py               # Application entry point
/requirements.txt      # Python dependencies
```

### Development Workflow

1. Define domain layer first (entities, value objects, aggregates)
2. Write domain tests
3. Implement repositories
4. Build use cases
5. Create API endpoints
6. Add integration tests

### Testing

```bash
pytest tests/
pytest tests/ -v  # Verbose
pytest tests/ --cov=src  # With coverage
```
