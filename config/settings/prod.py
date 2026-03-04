import dj_database_url

from .common import *

DEBUG = False

ALLOWED_HOSTS = ["jobtoinvoiceapp-backend.onrender.com"]

# Security settings
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


# CORS - restrict to frontend domain
CORS_ALLOWED_ORIGINS = [
    "https://jobtoinvoiceapp-frontend.vercel.app",
]

CORS_ALLOW_CREDENTIALS = True


DATABASES = {"default": dj_database_url.config(default=os.getenv("DATABASE_URL"))}
