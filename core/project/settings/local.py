from .main import *  # noqa


DEBUG = True

ALLOWED_HOSTS = [
    "127.0.0.1",
    "192.168.1.36",  # Windows
    "10.1.30.46",  # Windows
    "192.168.1.42",  # Ubuntu
    "192.168.1.34"
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

AUTH_USER_MODEL = "account.User"

# Для автоматического создания групп
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# Редиректы
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/profile/"
LOGOUT_REDIRECT_URL = ""

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],  # Для Docker или [("localhost", 6379)]
        },
    },
}
