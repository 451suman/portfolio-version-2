
import os
from pathlib import Path

from django.contrib.messages import constants as messages
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-change-this-in-production"
)

DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = [
    "sumancodes.pythonanywhere.com",
    "localhost",
    "127.0.0.1",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "accounts",
    "core",
    "blog",
    "portfolio",
    "contact",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "portfolio_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.site_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "portfolio_project.wsgi.application"

# DATABASE
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_USER_MODEL = "accounts.CustomUser"

# PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# INTERNATIONALIZATION
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ==========================================
# STATIC FILES
# ==========================================

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# ==========================================
# MEDIA FILES
# ==========================================

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ==========================================
# LOGIN
# ==========================================

LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "core:home"
LOGOUT_REDIRECT_URL = "core:home"

# ==========================================
# MESSAGES
# ==========================================

MESSAGE_TAGS = {
    messages.DEBUG: "debug",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "danger",
}

# ==========================================
# SITE SETTINGS
# ==========================================

SITE_NAME = os.environ.get("SITE_NAME")
SITE_DESCRIPTION = os.environ.get("SITE_DESCRIPTION")
SITE_AUTHOR = os.environ.get("SITE_AUTHOR")

SITE_EMAIL = os.environ.get("SITE_EMAIL")
SITE_PHONE = os.environ.get("SITE_PHONE")
SITE_ADDRESS = os.environ.get("SITE_ADDRESS")

ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL")

# ==========================================
# EMAIL SETTINGS
# ==========================================

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))

EMAIL_USE_TLS = (
    os.environ.get("EMAIL_USE_TLS", "False").lower() == "true"
)

EMAIL_USE_SSL = (
    os.environ.get("EMAIL_USE_SSL", "False").lower() == "true"
)

EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

EMAIL_SSL_KEYFILE = None
EMAIL_SSL_CERTFILE = None

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# ==========================================
# DEFAULT PRIMARY KEY
# ==========================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
