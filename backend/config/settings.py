"""
Django settings for config project.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Cargar variables de entorno desde el archivo .env
load_dotenv(BASE_DIR / '.env')

# ==========================================
# SEGURIDAD (Variables dinámicas)
# ==========================================
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default-key-1234')

# True en local, False si la variable en .env dice 'False'
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*'] # En producción, cambia esto por tu dominio

# ==========================================
# APLICACIONES Y MIDDLEWARE
# ==========================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Terceros
    'rest_framework',
    'drf_spectacular',
    'corsheaders',
    'django_filters', # Importante para que funcionen los filtros

    # Locales
    'users',
    'inventory',
    'bookings',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ==========================================
# BASE DE DATOS (Dinámica para Docker)
# ==========================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'postgres'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', '935475'),
        # Si no encuentra DB_HOST en el .env, usa 'localhost'
        'HOST': os.environ.get('DB_HOST', 'localhost'), 
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# ==========================================
# AUTENTICACIÓN Y MODELO DE USUARIO
# ==========================================
AUTH_USER_MODEL = 'users.CustomUser' 

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ==========================================
# CONFIGURACIÓN DRF Y SWAGGER
# ==========================================
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'users.authentication.FirebaseAuthentication', 
        'rest_framework.authentication.SessionAuthentication', 
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Mi API de Django',
    'DESCRIPTION': 'Documentación de la API para mi proyecto',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# ==========================================
# CORS
# ==========================================
# En desarrollo permitimos todo. En producción, usa CORS_ALLOWED_ORIGINS
CORS_ALLOW_ALL_ORIGINS = True 

# ==========================================
# INTERNACIONALIZACIÓN
# ==========================================
LANGUAGE_CODE = 'es-ec'
TIME_ZONE = 'America/Guayaquil'
USE_I18N = True
USE_TZ = True

# ==========================================
# ARCHIVOS ESTÁTICOS Y MEDIA
# ==========================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Útil para recolectar estáticos en Docker

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')