#!/bin/bash
set -e

until psql -U "${POSTGRES_USER}" -d data_pipeline_db -c '\q'; do
  >&2 echo "data_pipeline_db is not yet available - sleeping"
  sleep 1
done


psql -U "${POSTGRES_USER}" -d data_pipeline_db <<-EOSQL
    CREATE SCHEMA IF NOT EXISTS raw_data;
    CREATE SCHEMA IF NOT EXISTS data_quality;
    CREATE SCHEMA IF NOT EXISTS curated_data;
    CREATE SCHEMA IF NOT EXISTS analytics;
EOSQL
