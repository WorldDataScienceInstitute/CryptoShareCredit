"""
Django settings for ATM project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
import django_heroku
from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-1he#65^9)$u1rfq++qax+q8te-!*54ia93itmz0al!fipu7&+_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'atm_functions',
    'authentication',
]

MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django_session_timeout.middleware.SessionTimeoutMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'moesifdjango.middleware.moesif_middleware',
    'authentication.middleware.IPFilterMiddleware',
]

ROOT_URLCONF = 'ATM.urls'

if not os.environ.get('testing'):
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'ATM.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR/'static'
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = ('whitenoise.storage.CompressedManifestStaticFilesStorage')

# Session settings
# https://docs.djangoproject.com/en/3.2/ref/settings/#sessions
# https://github.com/labd/django-session-timeout

# session timeout after 5 minutes of inactivity
SESSION_EXPIRE_SECONDS = 60*5
# user activity resets session expiration timer
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
# redirect to logout page after session times out
SESSION_TIMEOUT_REDIRECT = '/Logout/'

# sign user out after an hour
SESSION_COOKIE_AGE = 60*60

# SMTP/email configuration
EMAIL_HOST = 'mail.cryptoshareapp.com'
EMAIL_HOST_USER = 'help@cryptoshareapp.com'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'help@cryptoshareapp.com'
EMAIL_PORT = 587
NO_REPLY_PASSWORD = os.environ['NO_REPLY_PASSWORD']
X_FRAME_OPTIONS = 'SAMEORIGIN'

# LOGIN_URL = 'authentication:Login'
LOGIN_URL = 'atm_functions:Home'

#CELERY config
# CELERY_BROKER_URL = 'redis://:p334a76fb64842055b48d0a15b2c5642e87b8ba2a89e8ad4717d2d078520af750@ec2-50-17-230-60.compute-1.amazonaws.com:29899'
CELERY_BROKER_URL = os.environ['REDIS_URL']

#Moesif config
def identifyUser(req, res):
    if req.user and req.user.is_authenticated:
        return req.user.username
    else:
        return None

MOESIF_MIDDLEWARE = {
    'APPLICATION_ID': 'eyJhcHAiOiI3MTA6Njc1IiwidmVyIjoiMi4wIiwib3JnIjoiMTYzOjI1OSIsImlhdCI6MTY1MTM2MzIwMH0.Tq7DPB2d6yeyiUCqwJLgJmk2OMfwaBjljrBVxotG9oo',

    'CAPTURE_OUTGOING_REQUESTS': True, # Set to True to also capture outgoing calls to 3rd parties.

    'IDENTIFY_USER': identifyUser # Optional hook to link API calls to users
}


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

django_heroku.settings(locals())
