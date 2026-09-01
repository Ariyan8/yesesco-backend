import sys
import os

# اضافه کردن مسیر ریشه پروژه به sys.path
# این کار باعث می‌شود که پایتون بتواند ماژول‌های داخل پوشه 'app' را پیدا کند
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# اطمینان از اینکه پوشه app در مسیر قرار دارد
if os.path.abspath('./app') not in sys.path:
    sys.path.insert(1, os.path.abspath('./app'))

# ایمپورت کردن اپلیکیشن FastAPI از app.main
try:
    from app.main import app
except ModuleNotFoundError:
    # fallback در صورت نیاز به اجرای مستقیم
    from main import app

# ورسل به دنبال متغیر application یا app در سطح بالا می‌گردد
application = app
__all__ = ["app", "application"]
