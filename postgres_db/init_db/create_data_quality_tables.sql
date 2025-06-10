CREATE SCHEMA IF NOT EXISTS data_quality;

CREATE TABLE IF NOT EXISTS data_quality.validation_results (
    validation_id SERIAL PRIMARY KEY,
    batch_id VARCHAR(255) NOT NULL,
    expectation_suite_name VARCHAR(255) NOT NULL,
    validation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    success BOOLEAN NOT NULL,
    results JSONB,
    meta JSONB
);

CREATE TABLE IF NOT EXISTS data_quality.data_quarantine (
    quarantine_id SERIAL PRIMARY KEY,
    table_name VARCHAR(255) NOT NULL,
    record_id VARCHAR(255),
    data_content JSONB NOT NULL,
    reason TEXT,
    quarantine_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);