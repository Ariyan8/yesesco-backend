import sys
import os

# اضافه کردن مسیر ریشه پروژه به sys.path جهت لود شدن ماژول app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

# تعریف پاسخ برای تمام آدرس‌های ریشه احتمالی که ورسل فوروارد می‌کند
@app.get("/")
@app.get("/api")
@app.get("/api/index.py")
def read_root():
    return {
        "status": "online",
        "message": "YesESCo API is running successfully on Vercel"
    }
