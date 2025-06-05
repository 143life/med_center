from .main import *  # noqa


# Отключаем режим отладки
DEBUG = False

ALLOWED_HOSTS = env.list(  # noqa
    "ALLOWED_HOSTS",
    default=[
        "127.0.0.1",
    ],
)

# Настройки безопасности (временно отключаем HTTPS-only настройки)
SECURE_SSL_REDIRECT = False  # Временно отключаем, пока нет SSL
SESSION_COOKIE_SECURE = False  # Временно отключаем, пока нет SSL
CSRF_COOKIE_SECURE = False  # Временно отключаем, пока нет SSL
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Настройки CSRF (разрешаем HTTP пока нет HTTPS)
CSRF_TRUSTED_ORIGINS = [
    "http://smtu-med.ru",
    "http://www.smtu-med.ru",
    "http://localhost",
]

# Content Security Policy
CSP_DEFAULT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "'unsafe-eval'")
CSP_IMG_SRC = ("'self'", "data:", "https:")
CSP_CONNECT_SRC = (
    "'self'",
    "ws://smtu-med.ru",
    "ws://www.smtu-med.ru",
    "ws://localhost",
    "http://smtu-med.ru",
    "http://www.smtu-med.ru",
    "http://localhost",
)

# Настройки статических и медиа файлов
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"  # noqa

# Настройки WebSocket
WEBSOCKET_CONNECT_TIMEOUT = 30
WEBSOCKET_READ_TIMEOUT = 30

# Настройки очереди
QUEUE_UPDATE_INTERVAL = 10  # секунды
MAX_QUEUE_SIZE = 10

# Настройки Celery
CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = "redis://redis:6379/0"
CELERY_TIMEZONE = "Europe/Moscow"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 минут

CELERY_IMPORTS = (
    "core.apps.medcenter.tasks",
)  # Явное указание модуля с задачами

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

# Настройки логирования
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",  # noqa
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs/django.log",  # noqa
            "formatter": "verbose",
        },
        "console": {
            "level": "ERROR",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file", "console"],
            "level": "ERROR",
            "propagate": True,
        },
        "core.apps.medcenter": {
            "handlers": ["file", "console"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}

# Настройки Channels
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
            "capacity": 1500,  # Максимальное количество сообщений в очереди
            "expiry": 10,  # Время жизни сообщений (секунды)
        },
    },
}

# Настройки аутентификации
AUTH_USER_MODEL = "account.User"
AUTHENTICATION_BACKENDS = [
    "core.apps.account.backends.EmailAuthBackend",
    "django.contrib.auth.backends.ModelBackend",
]

# Настройки URL
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "account:profile"
LOGOUT_REDIRECT_URL = "/"

# API настройки
API_BASE_URL = "http://localhost:8000/api/v1/"

# Дополнительные настройки безопасности
X_FRAME_OPTIONS = "DENY"  # Запрещаем встраивание сайта в iframe
