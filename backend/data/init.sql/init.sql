-- Create sectors table
CREATE TABLE sectors (
    id SERIAL PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL,
    name_ar VARCHAR
);

-- Create markets table
CREATE TABLE markets (
    id SERIAL PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL,
    name_ar VARCHAR
);

-- Create ipo_types table
CREATE TABLE ipo_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL,
    name_ar VARCHAR
);

-- Create ipo_statuses table
CREATE TABLE ipo_statuses (
    id SERIAL PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL,
    name_ar VARCHAR
);

-- Create ipos table
CREATE TABLE ipos (
    id SERIAL PRIMARY KEY,
    name VARCHAR,
    name_ar VARCHAR,
    url VARCHAR,
    status VARCHAR,
    status_ar VARCHAR,
    attachment VARCHAR,
    type VARCHAR,
    type_ar VARCHAR,
    market VARCHAR,
    market_ar VARCHAR,
    sector VARCHAR,
    sector_ar VARCHAR,
    market_url VARCHAR,
    volume INTEGER,
    announced_at TIMESTAMP,
    sector_id INTEGER REFERENCES sectors(id),
    market_id INTEGER REFERENCES markets(id),
    type_id INTEGER REFERENCES ipo_types(id),
    status_id INTEGER REFERENCES ipo_statuses(id),
    stock_id INTEGER REFERENCES stocks(id)
);

-- Create indexes for ipos
CREATE INDEX idx_ipos_announced_at ON ipos (announced_at);

-- Alter stocks table to use foreign keys
ALTER TABLE stocks ADD COLUMN sector_id INTEGER REFERENCES sectors(id);
ALTER TABLE stocks ADD COLUMN market_id INTEGER REFERENCES markets(id);
-- Note: Remove old columns after migration if needed
