# Collector Microservice

This is the data collection microservice for ZH.MarketPulse.EGX, responsible for fetching stock data from Mubasher APIs.

## Features

- **Stock Data Collection**: Fetches stock listings from both Arabic and English Mubasher endpoints
- **Bilingual Support**: Merges Arabic and English stock data
- **REST API**: FastAPI-based endpoints for triggering collection
- **Docker Support**: Containerized deployment with PostgreSQL
- **Health Monitoring**: Built-in health checks and monitoring

## API Endpoints

- `GET /` - Service information
- `GET /health` - Health check
- `POST /collect/stocks` - Trigger background stock collection
- `GET /collect/stocks/sync` - Trigger synchronous stock collection
- `GET /config` - Get collector configuration

## Running Locally

```bash
# Install dependencies
pip install -r ../requirements.txt

# Run the service
python ../run_collector.py
```

## Running with Docker

```bash
# Build and run with docker-compose
docker-compose up --build
```

## Environment Variables

- `DATABASE_URL` - PostgreSQL connection string
- `COLLECTOR_PORT` - Service port (default: 8001)
- `COLLECTOR_HOST` - Service host (default: 0.0.0.0)
- `LOG_LEVEL` - Logging level (default: INFO)

## API Documentation

When running, visit `http://localhost:8001/docs` for interactive API documentation.