import dj_database_url

from .common import *

DEBUG = False

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# CORS - restrict to frontend domain
CORS_ALLOWED_ORIGINS = [
    "https://jobtoinvoiceapp-frontend.onrender.com",
]

CORS_ALLOW_ALL_ORIGINS = False


DATABASES = {"default": dj_database_url.config(default=os.getenv("DATABASE_URL"))}
