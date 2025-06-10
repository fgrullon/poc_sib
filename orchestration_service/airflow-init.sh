#!/bin/bash
set -e

until pg_isready -h postgres_db -p 5432 -U superset; do
  sleep 1
done

airflow db migrate || true
airflow db upgrade || true

airflow users create \
    --username admin \
    --firstname Peter \
    --lastname Parker \
    --role Admin \
    --email spiderman@superhero.org \
    --password admin || true


exec airflow "$@"
