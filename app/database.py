import os
import ssl
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

load_dotenv()

# مقدار پیش‌فرض در صورت نبود متغیر محیطی
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:123456@localhost:5432/yesesco_db"
)

# اصلاح خودکار پروتکل برای درایور asyncpg
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
elif DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)

# تمیزکاری پارامترهای ناسازگار از کوئری‌استرینگ
for param in ["?sslmode=require", "&sslmode=require", "?ssl=true", "&ssl=true"]:
    DATABASE_URL = DATABASE_URL.replace(param, "")

# تنظیمات اتصال پیشرفته برای سازگاری با Supabase و محیط‌های Serverless
connect_args = {}

# برای اتصال به سرویس‌های ابری مثل Supabase یا Neon
if "supabase" in DATABASE_URL or "neon.tech" in DATABASE_URL or "pooler" in DATABASE_URL:
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    connect_args["ssl"] = ssl_context
    # ضروری برای Supabase Transaction Pooler (پورت 6543)
    connect_args["prepared_statement_cache_size"] = 0

# ساخت موتور اتصال Async
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    connect_args=connect_args,
    pool_pre_ping=True,      # تست سلامت اتصال قبل از ارسال کوئری
    pool_recycle=300         # بازنشانی اتصال‌های غیرفعال هر ۵ دقیقه
)

# ایجاد Factory برای Sessionهای ناهمگام
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# کلاس پایه برای مدل‌های دیتابیس (SQLAlchemy Base)
Base = declarative_base()

# وابستگی (Dependency) جهت تزریق سشن به روت‌های FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
