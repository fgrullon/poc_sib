import os

class Config:
    ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "YOUR_ALPHA_VANTAGE_API_KEY")

    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres_db")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "YOUR_POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "YOUR_POSTGRES_PASSWORD")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "data_pipeline_db")
