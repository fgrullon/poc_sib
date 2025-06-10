#!/bin/bash
set -e


superset db upgrade

echo "Creating Superset admin user..."
superset fab create-admin --username admin --firstname Superset --lastname Admin --email admin@superset.com --password admin || true

echo "Initializing Superset roles and permissions..."
superset init

echo "Superset initialization complete. Starting Gunicorn..."

exec "$@"
