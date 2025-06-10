CREATE SCHEMA IF NOT EXISTS analytics;

CREATE TABLE IF NOT EXISTS analytics.fact_financial_metrics_annual (
    company_symbol VARCHAR(50),
    fiscal_year INT,
    total_revenue NUMERIC,
    net_income NUMERIC,
    total_assets NUMERIC,
    operating_cash_flow NUMERIC,
    avg_cpi NUMERIC,
    avg_inflation NUMERIC,
    avg_retail_sales NUMERIC,
    _processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (company_symbol, fiscal_year)
);

CREATE TABLE IF NOT EXISTS analytics.dim_companies (
    company_symbol VARCHAR(50) PRIMARY KEY,
    company_name VARCHAR(255),
    company_sector VARCHAR(255),
    company_industry VARCHAR(255),
    company_country VARCHAR(50),
    company_currency VARCHAR(10),
    _processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS analytics.dim_date (
    date_key DATE PRIMARY KEY,
    year INT,
    quarter INT,
    month INT,
    day INT,
    _processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_fact_company_symbol ON analytics.fact_financial_metrics_annual (company_symbol);
CREATE INDEX IF NOT EXISTS idx_fact_fiscal_year ON analytics.fact_financial_metrics_annual (fiscal_year);