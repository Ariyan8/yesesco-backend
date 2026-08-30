import sys
import os

# اضافه کردن دایرکتوری اصلی به مسیر پایتون
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
