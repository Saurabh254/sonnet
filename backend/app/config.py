import os
from typing import Literal

from pydantic import PostgresDsn

POSTGRES_USER: str = "postgres"
POSTGRES_PWD: str = "12345678"
POSTGRES_HOST: str = "localhost"
POSTGRES_PORT: int = 5432
POSTGRES_DATABASE: str = "sonnet"
DATABASE_ASYNC_POOL_SIZE: int = 50
DATABASE_SYNC_POOL_SIZE: int = 50
DATABASE_POOL_RECYCLE_SECONDS: int = 600  # 10 minutes


def get_postgres_dsn(driver: Literal["asyncpg", "psycopg2"]) -> str:
    return str(
        PostgresDsn.build(  # type: ignore
            scheme=f"postgresql+{driver}",
            username=POSTGRES_USER,
            password=POSTGRES_PWD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            path=POSTGRES_DATABASE,
        )
    )
