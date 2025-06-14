

from pathlib import Path

import os

from .jazzmin import JAZZMIN_SETTINGS 
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "django-insecure-c&7t#9g=*9(b2*_h3$zb!$vko0xffi0+=omr=dalbeyrefk87t"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['auteur-bd.bilili-bd.com', 'bilili-bd.com', 'localhost']
#'auteur-bd.bilili-bd.com', 'bilili-bd.com', 'localhost'
# Celestin2001.pythonanywhere.com'
X_FRAME_OPTIONS = 'ALLOWALL'
# CSRF_TRUSTED_ORIGINS = [
#     "https://5610-197-149-245-198.ngrok-free.app",
#     "https://*.ngrok.io"  # Permet toutes les URLs Ngrok
# ]

# CELERY_BROKER_URL = 'redis://localhost:6379/0'  # URL de Redis
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_TIMEZONE = 'UTC'

# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gestion_content',
    'gestion_utilisateur',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

ROOT_URLCONF = 'Gestion_BD.urls'

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

WSGI_APPLICATION = 'Gestion_BD.wsgi.application'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'bililibdfestival$auteur_bd',  # le nom exact de ta base sur PythonAnywhere
#         'USER': 'bililibdfestival',      # ton username PA
#         'PASSWORD': 'bdauteur',        # le mot de passe MySQL donné par PA
#         'HOST': 'bililibdfestival.mysql.pythonanywhere-services.com',  # très important
#         'PORT': '3306',                  # port MySQL
#     }
# }


import os

# Détecter si on est en local ou en production
IS_PRODUCTION = os.environ.get('PYTHONANYWHERE_DOMAIN') is not None

if IS_PRODUCTION:
    # Configuration pour PythonAnywhere (Production)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'bililibdfestival$bililifestival',  #  nom de ma base de données sur PythonAnywhere
            'USER': 'bililibdfestival',     # mon nom d'utilisateur PythonAnywhere
            'PASSWORD': 'bdauteur',       # mot de passe MySQL donné par PythonAnywhere
            'HOST': 'bililibdfestival.mysql.pythonanywhere-services.com', # hôte MySQL
            'PORT': '3306',             # port MySQL
        }
    }
else:
    # Configuration locale (Développement avec SQLite)
    DATABASES = {
       'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'bd_auteur',  # Remplace par le nom réel de ta base MySQL
            'USER': 'celestin',    # Remplace par ton utilisateur MySQL
            'PASSWORD': 'bdauteur', # Remplace par ton mot de passe MySQL
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'jeremiesandouno123@gmail.com'
EMAIL_HOST_PASSWORD = 'idwpftboferfwfbc'
# idwpftboferfwfbc
# lglcsiyshbbtekrm

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

AUTH_USER_MODEL = 'gestion_utilisateur.Utilisateur'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/



# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



