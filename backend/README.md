# Orbit Eclipse Backend

FastAPI backend for computing orbital eclipse durations.

## Setup

```bash
# Create virtual environment
uv venv

# Install package in editable mode
uv pip install -e .

# Run development server
uv run uvicorn app.main:app --reload --port 8000
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

```bash
# Install dev dependencies
uv pip install -e ".[dev]"

# Run linter
uv run ruff check .

# Run type checker
uv run mypy app

# Run tests
uv run pytest
```
