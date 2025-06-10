CREATE SCHEMA IF NOT EXISTS curated_data;

CREATE TABLE IF NOT EXISTS curated_data.companies (
    symbol VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255),
    sector VARCHAR(255),
    industry VARCHAR(255),
    country VARCHAR(50),
    currency VARCHAR(10),
    latest_quarter DATE,
    market_capitalization NUMERIC,
    _loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS curated_data.financial_reports_annual (
    symbol VARCHAR(50),
    fiscal_date_ending DATE,
    report_type VARCHAR(50),
    reported_currency VARCHAR(10),
    metric_name VARCHAR(255),
    metric_value NUMERIC,
    _loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (symbol, fiscal_date_ending, report_type, metric_name)
);

CREATE TABLE IF NOT EXISTS curated_data.economic_indicators (
    indicator_date DATE PRIMARY KEY,
    cpi_value NUMERIC,
    inflation_value NUMERIC,
    retail_sales_value NUMERIC,
    _loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);