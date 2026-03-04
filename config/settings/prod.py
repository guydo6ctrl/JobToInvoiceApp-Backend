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
    "https://localhost:5173/",
]

CORS_ALLOW_ALL_ORIGINS = False

DATABASE_URL = "postgresql://jobtoinvoiceapp_db_user:7Mfw5Q8OGDLGls97kmfx3aj8QqLYMakX@dpg-d6k0ncua2pns738119c0-a.oregon-postgres.render.com/jobtoinvoiceapp_db"

DATABASES = {"default": dj_database_url.config(default=os.getenv("DATABASE_URL"))}
