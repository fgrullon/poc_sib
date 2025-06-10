# Use a Python 3.9 image as the base
FROM python:3.9-slim-buster

# Set the working directory inside the container
# This is where your app's main files will reside
WORKDIR /app

# Install system dependencies (build-essential, libpq-dev for psycopg2, python3-dev)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Install pip and upgrade it to ensure it's up-to-date
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy requirements.txt and install Python dependencies FIRST to leverage Docker caching
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the 'app' subdirectory into the container's /app directory
# This assumes main.py is inside the 'app' directory on your host
COPY ./app .

# Copy the great_expectations configuration into the container's /app directory
COPY ./great_expectations /app/great_expectations

# Set environment variables for Great Expectations root directory
ENV GE_ROOT_DIR /app/great_expectations

# Define the command to run the data quality service
# Now main.py should be directly in /app
CMD ["python", "main.py"]