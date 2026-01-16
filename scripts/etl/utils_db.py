# scripts/etl/utils_db.py

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def get_engine() -> Engine:
    """
    Crea y retorna un engine SQLAlchemy para PostgreSQL.
    Ajustado al entorno local (Docker exposed port 5433).
    """
    user = "admin"
    password = "admin123"        # usa .env si luego lo deseas
    host = "localhost"
    port = 5433
    database = "contratistas"

    url = (
        f"postgresql+psycopg2://{user}:{password}"
        f"@{host}:{port}/{database}"
    )

    return create_engine(url, future=True)
