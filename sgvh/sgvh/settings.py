from pathlib import Path
import os  # Añadido para manejar rutas de archivos

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# En producción, deberías mover esto a una variable de entorno
SECRET_KEY = 'django-insecure-*jbj*g(^k==yk!xc#ylgld1w+@mp3h87+(cpoj9gg8c+a=w)!r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # Cambia a False en producción

ALLOWED_HOSTS = ['localhost', '127.0.0.1']  # Añade los hosts permitidos

# Application definition
INSTALLED_APPS = [
    'horarios',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sgvh.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Añadido para buscar templates en la raíz del proyecto
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

WSGI_APPLICATION = 'sgvh.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sgvh_db',  
        'USER': 'root',                 
        'PASSWORD': 'root',          
        'HOST': 'localhost',                  
        'PORT': '3306',                       
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Internationalization
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Bogota'  # Ajustado a la zona horaria de Colombia
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Añadido para colectar archivos estáticos
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # Añadido para buscar archivos estáticos adicionales

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración de redirección de login
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'admin_dashboard'
LOGOUT_REDIRECT_URL = 'login'

# Configuraciones adicionales de seguridad (activa estas en producción)
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True