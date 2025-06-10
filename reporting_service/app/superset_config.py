# superset_config.py
import os

SECRET_KEY = os.environ["SUPERSET_SECRET_KEY"]

DATABASE_HOSTNAME = os.environ.get("DATABASE_HOSTNAME", "localhost")
DATABASE_USERNAME = os.environ.get("DATABASE_USERNAME", "fgrullon")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD", "admin")
DATABASE_DB = os.environ.get("DATABASE_DB", "superset")

SQLALCHEMY_DATABASE_URI = (
    f"postgresql+psycopg2://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@"
    f"{DATABASE_HOSTNAME}:5432/{DATABASE_DB}"
)
