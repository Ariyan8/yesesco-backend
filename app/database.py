import os
import ssl

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL environment variable is not configured."
    )


if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://",
        "postgresql+asyncpg://",
        1,
    )
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://",
        "postgresql+asyncpg://",
        1,
    )
elif not DATABASE_URL.startswith("postgresql+asyncpg://"):
    raise RuntimeError(
        "DATABASE_URL must use PostgreSQL format."
    )


for parameter in (
    "?sslmode=require",
    "&sslmode=require",
    "?ssl=true",
    "&ssl=true",
):
    DATABASE_URL = DATABASE_URL.replace(parameter, "")


connect_args = {}

if any(
    hostname in DATABASE_URL
    for hostname in (
        "supabase.com",
        "pooler",
        "neon.tech",
    )
):
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    connect_args = {
        "ssl": ssl_context,
        "prepared_statement_cache_size": 0,
    }


engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    connect_args=connect_args,
    poolclass=NullPool,
)


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
