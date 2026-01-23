# Orbit Eclipse Calculator

A web application that computes orbital eclipse durations for circular Earth orbits.

## Features

- Compute orbital period from altitude
- Calculate eclipse duration using cylindrical Earth shadow approximation
- Plot eclipse duration over a year based on beta angle vs time
- Visualize results with interactive Plotly charts

## Quick Start

### Prerequisites

- Python 3.12+
- Node.js 18+
- [uv](https://github.com/astral-sh/uv) package manager

### Backend (Terminal 1)

```bash
cd backend
uv venv
uv pip install -e .
uv run uvicorn app.main:app --reload --port 8000
```

Backend runs at: http://localhost:8000

### Frontend (Terminal 2)

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: http://localhost:5173

## API Endpoints

- `GET /health` - Health check
- `POST /api/eclipse/circular` - Compute eclipse for given beta angle
- `POST /api/eclipse/yearly` - Compute yearly eclipse curve

## Tech Stack

- **Backend**: Python, FastAPI, Pydantic
- **Frontend**: React, TypeScript, Vite, Plotly
