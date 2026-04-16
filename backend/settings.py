import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'dev-secret-key-change-me')
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')


def _csv_env(name, default=''):
    raw = os.getenv(name, default)
    return [item.strip() for item in raw.split(',') if item.strip()]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'api',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'urls'
TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [], 'APP_DIRS': True, 'OPTIONS': {'context_processors': ['django.template.context_processors.request', 'django.contrib.auth.context_processors.auth', 'django.contrib.messages.context_processors.messages']}}]
WSGI_APPLICATION = 'wsgi.application'
USE_SQLITE = os.getenv('USE_SQLITE', 'True').lower() == 'true'

if USE_SQLITE:
    # Default local mode to avoid hard dependency on MySQL during development.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': str(BASE_DIR / 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('MYSQL_DATABASE', 'book_intelligence'),
            'USER': os.getenv('MYSQL_USER', 'root'),
            'PASSWORD': os.getenv('MYSQL_PASSWORD', 'root'),
            'HOST': os.getenv('MYSQL_HOST', 'localhost'),
            'PORT': os.getenv('MYSQL_PORT', '3306'),
            'OPTIONS': {'charset': 'utf8mb4'},
        }
    }
LANGUAGE_CODE='en-us'
TIME_ZONE='UTC'
USE_I18N=True
USE_TZ=True
STATIC_URL='static/'
DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
CORS_ALLOW_ALL_ORIGINS = os.getenv('CORS_ALLOW_ALL_ORIGINS', 'True').lower() == 'true'
CORS_ALLOWED_ORIGINS = _csv_env('CORS_ALLOWED_ORIGINS')
CSRF_TRUSTED_ORIGINS = _csv_env('CSRF_TRUSTED_ORIGINS')
CACHE_TTL_SECONDS=int(os.getenv('CACHE_TTL_SECONDS','600'))
CHROMA_PERSIST_DIR=os.getenv('CHROMA_PERSIST_DIR', str(BASE_DIR / 'chroma_store'))
EMBEDDING_MODEL_NAME=os.getenv('EMBEDDING_MODEL_NAME','sentence-transformers/all-MiniLM-L6-v2')
LM_STUDIO_URL=os.getenv('LM_STUDIO_URL','http://localhost:1234/v1/chat/completions')
LM_STUDIO_MODEL=os.getenv('LM_STUDIO_MODEL','local-model')
SCRAPER_BASE_URL=os.getenv('SCRAPER_BASE_URL','https://books.toscrape.com/catalogue/page-1.html')
