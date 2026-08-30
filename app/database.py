import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:123456@localhost:5432/yesesco_db"
)

# اصلاح خودکار پروتکل برای درایور asyncpg
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
elif DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)

# حذف پارامتر sslmode در صورت وجود برای جلوگیری از ارور asyncpg
if "sslmode=" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("?sslmode=require", "").replace("&sslmode=require", "")

# تنظیمات اتصال
connect_args = {}
if "neon.tech" in DATABASE_URL or "supabase" in DATABASE_URL or "ssl=true" in DATABASE_URL.lower():
    connect_args = {"ssl": True}

# ساخت موتور اتصال Async به دیتابیس
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    connect_args=connect_args,
    pool_pre_ping=True
)

# سشن برای اجرای کوئری‌ها
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# کلاس پایه برای مدل‌ها
Base = declarative_base()

# Dependency تزریق سشن دیتابیس
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
