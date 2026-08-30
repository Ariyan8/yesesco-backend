import sys
import os

# اضافه کردن مسیر ریشه پروژه به sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
