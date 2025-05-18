from .main import *  # noqa


DEBUG = True

ALLOWED_HOSTS = [
    "127.0.0.1",
    "192.168.1.46",  # Windows
    "10.1.30.46",  # Windows
    "192.168.1.42",  # Ubuntu
]

CSP_CONNECT_SRC = ["'self'", "ws://127.0.0.1:8000"]

SECURE_CONTENT_SECURITY_POLICY = "connect-src 'self' ws://127.0.0.1:8000;"

API_BASE_URL = "http://127.0.0.1:8000/api/v1/"

CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = "redis://redis:6379/0"
CELERY_TIMEZONE = "Europe/Moscow"

CELERY_IMPORTS = (
    "core.apps.medcenter.tasks",
)  # Явное указание модуля с задачами
