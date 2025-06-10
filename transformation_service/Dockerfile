FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -y git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --timeout 300 -r requirements.txt

ENV DBT_PROFILES_DIR=/app/dbt_project

CMD ["dbt", "debug", "--project-dir", "/app/dbt_project"]