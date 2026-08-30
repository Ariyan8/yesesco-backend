import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:123456@localhost:5432/yesesco_db"
)

# ساخت موتور اتصال Async به دیتابیس
engine = create_async_engine(DATABASE_URL, echo=True)

# سشن برای اجرای کوئری‌ها
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# کلاس پایه برای ساخت مدل‌ها
Base = declarative_base()

# Dependency تزریق سشن دیتابیس در Endpointها
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
