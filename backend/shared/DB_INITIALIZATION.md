# Database Initialization

This script handles the initial setup and seeding of the MarketPulse EGX database.

## Usage

### Basic Initialization
```bash
# Initialize database (creates tables and seeds data)
python backend/shared/init_db.py
```

### Force Re-initialization
```bash
# Force re-initialization even if database is not empty
python backend/shared/init_db.py --force
```

### Config Only
```bash
# Only seed configuration data, skip sample data
python backend/shared/init_db.py --config-only
```

## What It Does

1. **Checks Database Connection**: Verifies the database is accessible
2. **Creates Schema**: Creates all tables defined in the models
3. **Seeds Configuration**: Loads default configs from `fixtures/default_config.json`
4. **Seeds Sample Data**: Loads sample stocks from `fixtures/sample_stocks.json`

## Fixture Files

Place JSON files in `backend/shared/fixtures/` for automatic seeding:

- `default_config.json` - Default configuration values
- `sample_stocks.json` - Sample stock data for development
- `sample_news.json` - Sample news articles (future)
- `sample_indicators.json` - Sample technical indicators (future)

## Integration

Call this script at application startup:

```python
from backend.shared.init_db import DatabaseInitializer

# Initialize database on startup
initializer = DatabaseInitializer()
if not initializer.initialize_database():
    # Handle initialization failure
    exit(1)
```

## Environment Variables

Make sure `DATABASE_URL` is set:

```bash
export DATABASE_URL="postgresql://user:password@localhost/marketpulse_db"
```