import sys
import os

# اضافه کردن ریشه پروژه به مسیرهای پایتون
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

# ایجاد متغیرهای سطح بالا برای تشخیص ورسل
application = app
__all__ = ["app", "application"]
