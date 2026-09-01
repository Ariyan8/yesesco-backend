import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

load_dotenv()

# دریافت URL دیتابیس از Environment Variables
DATABASE_URL = os.getenv("DATABASE_URL", "")

# تبدیل فرمت postgresql:// به postgresql+asyncpg:// برای کار با درایور غیرهمگام
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
elif DATABASE_URL.startswith("postgresql://") and not DATABASE_URL.startswith("postgresql+asyncpg://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# حذف پارامتر sslmode چون asyncpg از آن پشتیبانی مستقیم در کوئری‌استرینگ نمی‌کند
if "?" in DATABASE_URL:
    base_url, _ = DATABASE_URL.split("?", 1)
    DATABASE_URL = base_url

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()
