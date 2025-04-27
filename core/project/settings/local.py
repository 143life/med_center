import os
from pathlib import Path

from .main import *  # noqa


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

DEBUG = True

ALLOWED_HOSTS = [
    "127.0.0.1",
    "192.168.1.46",  # Windows
    "10.1.30.46",  # Windows
    "192.168.1.42",  # Ubuntu
]

CORS_ALLOWED_ORIGINS = ["http://localhost:3000", "http://192.168.1.42:3000"]

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static_src")]

# noqa TEMPLATES[0]["OPTIONS"]["debug"] = True
