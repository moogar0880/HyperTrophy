"""
hyper_trophy.settings.py
===============

These settings are (or should be) generic to all environments.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/
TEMPLATE_DEBUG = DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
# This is *not* the production secret key.
SECRET_KEY = 'dev secret key'

ALLOWED_HOSTS = ['*'] if DEBUG else []

# Application definition
# Native Django Apps
DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.webdesign',
)

# Third-party Django packages
THIRD_PARTY_APPS = (
    'debug_toolbar',
    'bootstrap3'
)

# Apps developed for the HyperTrophy project
HYPER_APPS = (
    'hyper_trophy',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + HYPER_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# Route uWSGI and urls through HyperTrophy
ROOT_URLCONF = 'hyper_trophy.urls'

WSGI_APPLICATION = 'hyper_trophy.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Context Processors
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'hyper_trophy.context_processors.global_settings',
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
# Where collectstatic will collect files for deployment
STATIC_URL = '/static/'
# Where static files will be served from; could be an external site.
STATIC_ROOT = 'assets'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Logging
DEFAULT_LOGGER = 'logger'
TESTING_LOGGER = 'testing'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(module)s:%(lineno)s] "
                      "%(message)s",
        },
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(module)s:%(funcName)s:"
                      "%(lineno)s] %(message)s",
        }
    },
    'handlers': {
        'requests_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'requests.log',
            'formatter': 'standard'
        },
        'log_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'hyper_trophy.log',
            'backupCount': '5',
            'maxBytes': 1024 ** 2 * 10,  # 10 MB
            'formatter': 'standard'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'test_log_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'hyper_trophy.log',
            'mode': 'w',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'py.warnings': {
            'handlers': ['console']
        },
        'django.request': {
            'handlers': ['console', 'requests_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'logger': {
            'handlers': ['console', 'log_file'],
            'level': 'DEBUG',
        },
        'testing': {
            'handlers': ['console', 'test_log_file'],
            'level': 'DEBUG'
        }
    }
}
