from pathlib import Path
import os
from dotenv import load_dotenv

# =====================================================
# BASE
# =====================================================
BASE_DIR = Path(__file__).resolve().parent.parent

# =====================================================
# ENV
# =====================================================
load_dotenv()

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "unsafe-secret")

DEBUG = os.getenv("DJANGO_DEBUG", "0") == "1"

ALLOWED_HOSTS = os.getenv(
    "DJANGO_ALLOWED_HOSTS",
    "localhost,127.0.0.1,srni-backend.ngrok.io"
).split(",")

# =====================================================
# APPS
# =====================================================
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "corsheaders",
    "rest_framework",

    # Core
    "core",

    # Domains
    "apps.accounts",
    "apps.analytics",
    "apps.automatizacion_documental",
    "apps.colaboradores",
    "apps.dashboard",
    "apps.nlquery",

    # Integrations
    "sinapsis",
    "projects",
]

# =====================================================
# MIDDLEWARE
# =====================================================
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # Siempre primero
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# =====================================================
# URLS / WSGI
# =====================================================
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# =====================================================
# DATABASE
# =====================================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}

# =====================================================
# PASSWORD VALIDATORS
# =====================================================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# =====================================================
# INTERNACIONALIZACIÓN
# =====================================================
LANGUAGE_CODE = "es-co"
TIME_ZONE = "America/Bogota"
USE_I18N = True
USE_TZ = True

# =====================================================
# STATIC
# =====================================================
STATIC_URL = "/static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# =====================================================
# CORS
# =====================================================
CORS_ALLOWED_ORIGINS = [
    "https://srni-backend.ngrok.io",
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

# =====================================================
# CSRF
# =====================================================
CSRF_TRUSTED_ORIGINS = [
    "https://srni-backend.ngrok.io",
]

# ============================
# SESSION / CSRF COOKIES (NGROK)
# ============================

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "None"

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "None"

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False  # Necesario para que React pueda leer csrftoken

# =====================================================
# PROXY SETTINGS (IMPORTANTE DETRÁS DE NGINX / NGROK)
# =====================================================
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True
