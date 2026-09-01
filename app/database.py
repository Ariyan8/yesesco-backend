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
    # برای جلوگیری از خطای Build زمان استقرار در ورسل
    DATABASE_URL = "postgresql+asyncpg://postgres:dummy@localhost:5432/postgres"

# تبدیل پروتکل استاندارد به درایور asyncpg
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# پاکسازی پارامترهای تداخلی sslmode از query string
for parameter in ("?sslmode=require", "&sslmode=require", "?ssl=true", "&ssl=true"):
    DATABASE_URL = DATABASE_URL.replace(parameter, "")

# تنظیمات اتصال مخصوص Supabase Pooler (پورت 6543)
connect_args = {
    "prepared_statement_cache_size": 0,
    "statement_cache_size": 0,
}

# فعال‌سازی SSL context برای دیتابیس ریموت
if any(key in DATABASE_URL for key in ("supabase.com", "pooler", "neon.tech")):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    connect_args["ssl"] = ctx

# استفاده از NullPool در محیط سرورلس
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
    autocommit=False,
    autoflush=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
