# ZH.MarketPulse.EGX

ZH.MarketPulse.EGX is a proprietary software project authored by ZhEaIsNsAaBn, designed to analyze and predict trends in the Egyptian stock market (EGX). It collects historical data from sources like Mubasher, scrapes news from Mubasher, Arab Finance, and Alborsaanews, computes technical indicators, labels news for impact, cleans noisy data, and trains AI models to forecast price movements. Built as a personal development tool in Python with a React frontend, it emphasizes a modular pipeline for data-driven insights—ideal for private use or licensed applications. Market predictions are experimental and not financial advice; always consult professionals 💡.

**Key Features**:
- **Data Collection**: API pulls from Mubasher for stock names, Reuters codes, revenues, IPOs, and historical prices (from 2000 onward, often in 15-min candles).
- **News Scraping**: Extracts titles, bodies, dates, and tags from Mubasher (corporate results, sector updates), Arab Finance (MENA finance aggregates), and Alborsaanews (investment insights).
- **Analysis & Labeling**: Calculates indicators (RSI, moving averages, MACD); detects turning points; dual-labels news (outcome: up/down/flat; topic: revenue-beat, new factory via site tags or regex/spaCy).
- **AI Training**: Merges cleaned data into features; trains with scikit-learn or TensorFlow for predictions.
- **Frontend**: React app with TradingView Lightweight Charts for interactive stock visualizations, grids for lists, and panels for news/predictions.

**Tech Stack**: Python (pandas, BeautifulSoup/Selenium, SQLAlchemy, Loguru, scikit-learn/TensorFlow); React (Vite, Axios, Lightweight Charts for charts); Database (PostgreSQL).

**Limitations**: Relies on scraping (respect terms); predictions are for informational purposes only. Setup requires technical knowledge; contact the author for support or licensing inquiries.

### Folder Structure

The project is organized into backend (Python pipeline) and frontend (React app) components for modularity. Here's the complete tree:

| Folder/File                  | Description |
|------------------------------|-------------|
| **backend/**                 | All Python backend components for data pipeline and AI. |
| ├── **collector/**           | Data fetching microservice. |
| │   ├── **api/**             | FastAPI endpoints for the collector service. |
| │   │   ├── main.py          | FastAPI application with stock collection endpoints. |
| │   │   └── __init__.py      | API package exports. |
| │   ├── stocks.py            | API calls to Mubasher for stock listings (Arabic & English). |
| │   ├── Dockerfile           | Docker configuration for collector microservice. |
| │   ├── docker-compose.yml   | Docker Compose setup with PostgreSQL. |
| │   ├── .dockerignore        | Docker ignore file. |
| │   └── __init__.py          | Collector package exports. |
| ├── **sanitizer/**           | Data processing and cleaning. |
| │   └── sanitize.py          | Computes indicators (RSI, etc.), labels news, filters noise. |
| ├── **trainer/**             | AI model training. |
| │   └── train.py             | Loads cleaned data, trains models, saves to data/models/. |
| ├── **shared/**              | Common utilities and configuration. |
| │   ├── config_manager.py    | Configuration management with JSON defaults + DB overrides. |
| │   ├── db_engine.py         | SQLAlchemy database engine, sessions, and utilities. |
| │   ├── db_init.py           | Database initialization and seeding script. |
| │   ├── http_client.py       | Async HTTP client with retry logic and logging. |
| │   ├── logging.py           | Loguru configuration and timing decorator. |
| │   ├── retry.py             | Smart retry mechanism using tenacity. |
| │   ├── scrapers.py          | Web scraping utilities with Selenium and BeautifulSoup. |
| │   └── __init__.py          | Package exports. |
| ├── **data/**                | Database models and seed data. |
| │   ├── **models/**          | SQLAlchemy model definitions. |
| │   │   ├── __init__.py      | Model imports. |
| │   │   ├── stock.py         | Stock and StockPrice models. |
| │   │   ├── news.py          | News model for articles and sentiment. |
| │   │   ├── indicator.py     | Technical indicator models. |
| │   │   ├── training.py      | Training data and prediction models. |
| │   │   └── config.py        | Database-stored configuration model. |
| │   └── **seed/**            | JSON fixtures for database seeding. |
| │       ├── default_config.json | Default application configurations. |
| │       └── sample_stocks.json   | Sample EGX stock data. |
| ├── main.py                  | Orchestrates phases: collect → sanitize → train. |
| └── requirements.txt         | Python dependencies (httpx, tenacity, selenium, beautifulsoup4, etc.). |
| **frontend/**                | React application for UI and visualization. |
| ├── **src/**                 | Core frontend source. |
| │   ├── **components/**      | Reusable UI elements. |
| │   │   ├── Dashboard.js     | Layout for panels (charts, grids, news). |
| │   │   ├── StockChart.js    | TradingView Lightweight Charts for prices/indicators. |
| │   │   ├── StockGrid.js     | Grid for stock lists (e.g., with filtering). |
| │   │   ├── NewsFeed.js      | Displays labeled news with tags. |
| │   │   └── PredictionPanel.js | Shows AI forecasts as overlays/markers. |
| │   ├── **pages/**           | Route-based views. |
| │   │   └── Home.js          | Main dashboard aggregating data. |
| │   ├── **services/**        | API and utilities. |
| │   │   ├── api.js           | Axios wrappers for backend endpoints (e.g., getStocks()). |
| │   │   └── logger.js        | Frontend logging. |
| │   ├── **data/**            | Mock data for dev. |
| │   │   └── sampleStocks.json| EGX sample data for offline testing. |
| │   ├── App.js               | Root with routing and state (e.g., Context for stocks). |
| │   └── index.js             | Entry point. |
| ├── public/                  | Static assets (logos, etc.). |
| ├── vite.config.js           | Vite config (e.g., proxy to backend API). |
| └── package.json             | Dependencies (lightweight-charts, axios, etc.). |
| **data/**                    | Shared storage (raw JSONs, clean CSVs, models)—accessible by both if needed via API. |
| ├── raw/                     | Direct dumps from collection. |
| ├── clean/                   | Post-sanitization files. |
| └── models/                  | Trained AI outputs (.pkl/.h5). |
| README.md                    | Project documentation (this file). |

### Installation

1. Ensure Python 3.8+, Node.js, and PostgreSQL are installed.
2. Backend: Create a virtual env (`python -m venv venv && source venv/bin/activate`), then `pip install -r backend/requirements.txt`.
3. Database: Set up Postgres, create db (`createdb egx_db`), set `DATABASE_URL` environment variable (e.g., `export DATABASE_URL="postgresql://user:pass@localhost/egx_db"`).
4. Initialize Database: Run `python backend/shared/db_init.py` to create tables and seed initial data.
5. ChromeDriver: For Selenium web scraping; download from <https://chromedriver.chromium.org/> and add to PATH, or set path in config.
6. Frontend: `cd frontend`, `npm install`, `npm run dev`.

### Usage

- Backend pipeline: Run `python backend/main.py` for full execution or individual scripts for phases.
- Collector Microservice: Run `python backend/run_collector.py` to start the collector service on <http://localhost:8001>
- Collector API Docs: Visit <http://localhost:8001/docs> for interactive API documentation
- Frontend Development: Run `cd frontend && npm run dev` for development server on <http://localhost:5173>
- Full Stack with Docker: Use `docker-compose up --build` to run all services (frontend, collector, database)
- Database Initialization: Run `python backend/shared/db_init.py` to setup database and seed data.

### Frontend Details: React with TradingView Lightweight Charts

The frontend uses React (Vite) for a responsive dashboard, integrating TradingView's Lightweight Charts for high-performance stock visualizations. It's compact (~45 KB), supports candlesticks, indicators, and real-time updates—ideal for rendering EGX data with overlays for news events and predictions.

Example in `frontend/src/components/StockChart.js`:
```jsx
import { createChart } from 'lightweight-charts';
import { useEffect, useRef } from 'react';

function StockChart({ data }) {
  const chartRef = useRef();
  useEffect(() => {
    const chart = createChart(chartRef.current, { width: 600, height: 300 });
    const candleSeries = chart.addCandlestickSeries();
    candleSeries.setData(data); // e.g., [{ time: '2025-10-07', open: 12.3, high: 12.5, low: 12.1, close: 12.4 }]
    return () => chart.remove();
  }, [data]);
  return <div ref={chartRef} />;
}
```

Fetch data via services/api.js; add markers for turning points.

```jsx
import { createChart } from 'lightweight-charts';
import { useEffect, useRef } from 'react';

function StockChart({ data }) {
  const chartRef = useRef();
  useEffect(() => {
    const chart = createChart(chartRef.current, { width: 600, height: 300 });
    const candleSeries = chart.addCandlestickSeries();
    candleSeries.setData(data); // e.g., [{ time: '2025-10-07', open: 12.3, high: 12.5, low: 12.1, close: 12.4 }]
    return () => chart.remove();
  }, [data]);
  return <div ref={chartRef} />;
}
```

### License

### License

This software is proprietary and private. All rights reserved by ZhEaIsNsAaBn. Unauthorized use, distribution, or modification is prohibited. For licensing, paid access, or inquiries, contact the author. Not for free usage.

### Author

ZhEaIsNsAaBn—Available for private consultations or customizations.

