import environ

from .main import *  # noqa


# Содержит переменные окружения
env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")  # noqa

DEBUG = True

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
    "main-app",  # Имя сервиса в Docker
    "smtu-med.ru",
    "www.smtu-med.ru",
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
    "core.apps.account.backends.EmailAuthBackend",
    "django.contrib.auth.backends.ModelBackend",
]

# Редиректы
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "account:profile"
LOGOUT_REDIRECT_URL = ""

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],  # Для Docker или [("localhost", 6379)]
        },
    },
}

# Настройки кэширования
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SOCKET_TIMEOUT": 5,
            "SOCKET_CONNECT_TIMEOUT": 5,
            "CONNECTION_POOL_CLASS_KWARGS": {
                "max_connections": 50,
                "timeout": 20,
            },
            "PARSER_CLASS": "redis.connection.DefaultParser",
        },
    },
}

# Настройки сессий
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
