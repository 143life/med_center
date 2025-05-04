from .main import * # noqa

DEBUG = True

ALLOWED_HOSTS = [
    "127.0.0.1",
    "192.168.1.46",  # Windows
    "10.1.30.46",  # Windows
    "192.168.1.42",  # Ubuntu
]

CSP_CONNECT_SRC = ["'self'", "ws://127.0.0.1:8000"]

SECURE_CONTENT_SECURITY_POLICY = "connect-src 'self' ws://127.0.0.1:8000;"