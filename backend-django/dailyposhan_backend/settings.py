from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", "dailyposhan-dev-secret-key")
DEBUG = os.getenv("DEBUG", "True") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "apps.authentication",
    "apps.products",
    "apps.orders",
    "apps.payments",
    "apps.adminpanel",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "dailyposhan_backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": [
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
        ]},
    }
]

WSGI_APPLICATION = "dailyposhan_backend.wsgi.application"
ASGI_APPLICATION = "dailyposhan_backend.asgi.application"

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Parse DATABASE_URL for cloud databases (Heroku, etc.)
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600)
    }
else:
    # Local database configuration with individual settings
    DATABASE_ENGINE = os.getenv("DATABASE_ENGINE", "django.db.backends.sqlite3")
    DATABASE_NAME = os.getenv("DATABASE_NAME", BASE_DIR / "db.sqlite3")
    DATABASE_USER = os.getenv("DATABASE_USER", "")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "")
    DATABASE_HOST = os.getenv("DATABASE_HOST", "")
    DATABASE_PORT = os.getenv("DATABASE_PORT", "")

    DATABASES = {
        "default": {
            "ENGINE": DATABASE_ENGINE,
            "NAME": DATABASE_NAME,
            "USER": DATABASE_USER,
            "PASSWORD": DATABASE_PASSWORD,
            "HOST": DATABASE_HOST,
            "PORT": DATABASE_PORT,
            "OPTIONS": {},
        }
    }

    # Add database-specific options
    if DATABASE_ENGINE == "django.db.backends.postgresql":
        DATABASES["default"]["OPTIONS"] = {
            "sslmode": os.getenv("DATABASE_SSL_MODE", "require"),
        }
    elif DATABASE_ENGINE == "django.db.backends.mysql":
        DATABASES["default"]["OPTIONS"] = {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            "charset": "utf8mb4",
        }

# Database connection pooling and performance settings
DATABASES["default"]["CONN_MAX_AGE"] = int(os.getenv("DATABASE_CONN_MAX_AGE", "600"))
DATABASES["default"]["ATOMIC_REQUESTS"] = os.getenv("DATABASE_ATOMIC_REQUESTS", "False") == "True"

# Database backup settings
DATABASE_BACKUP_ENABLED = os.getenv("DATABASE_BACKUP_ENABLED", "False") == "True"
DATABASE_BACKUP_PATH = os.getenv("DATABASE_BACKUP_PATH", BASE_DIR / "backups")
DATABASE_BACKUP_RETENTION_DAYS = int(os.getenv("DATABASE_BACKUP_RETENTION_DAYS", "30"))

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CORS Configuration
CORS_ALLOWED_ORIGINS = [
    o.strip()
    for o in os.getenv(
        "CORS_ALLOWED_ORIGINS",
        "http://localhost:5173,http://localhost:5175,http://localhost:3000,http://127.0.0.1:5173,http://127.0.0.1:5175"
    ).split(",")
]
CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOW_CREDENTIALS = True
