"""
Django settings for img project.

Generated by 'django-admin startproject' using Django 1.10.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

from logging.handlers import SysLogHandler
import os
from os.path import basename

from django.core.urlresolvers import reverse_lazy

import getconf
from unipath import Path

# Build paths inside the project like this: BASE_DIR.child(...)
CONFIGURATION_APP_ROOT = Path(__file__).ancestor(1)
BASE_DIR = CONFIGURATION_APP_ROOT.ancestor(1)
PROJECT_ROOT = BASE_DIR.ancestor(1)
SITE_NAME = basename(PROJECT_ROOT)
PUBLIC_ROOT = PROJECT_ROOT.child('public')

CONFIG = getconf.ConfigGetter(SITE_NAME, [
    '/etc/%s/settings/' % SITE_NAME,
    PROJECT_ROOT.child('local_settings.ini'),
])

ENVIRONMENT = CONFIG.getstr('environment', 'dev')
assert ENVIRONMENT in ('prod', 'dev', 'test')


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = CONFIG.getstr('django.secret_key', 'unsecure')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = CONFIG.getbool('django.debug', ENVIRONMENT != 'prod')

ALLOWED_HOSTS = CONFIG.getlist('django.allowed_hosts')


# Application definition

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
)

THIRD_PARTY_APPS = (
    'pipeline',
    'widget_tweaks',
)

LOCAL_APPS = (
    'images',
    'memes',
    'img',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'pipeline.middleware.MinifyHTMLMiddleware', # TODO django-pipeline Django 1.10 support
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'img.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR.child('templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'images.context_processors.inappropriate_counter',
            ],
        },
    },
]

WSGI_APPLICATION = 'img.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': CONFIG.getstr('db.engine', 'django.db.backends.sqlite3'),
        'NAME': CONFIG.getstr('db.name', os.path.join(PROJECT_ROOT, 'img.sqlite3')),
        'USER': CONFIG.getstr('db.user'),
        'PASSWORD': CONFIG.getstr('db.password'),
        'HOST': CONFIG.getstr('db.host'),
        'PORT': CONFIG.getint('db.port'),
        'ATOMIC_REQUESTS': CONFIG.getbool('db.atomic_requests', True),
        'AUTOCOMMIT': CONFIG.getbool('db.autocommit', True),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = CONFIG.getstr('django.language_code', 'en-us')

TIME_ZONE = CONFIG.getstr('django.time_zone', 'UTC')

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_ROOT = CONFIG.getstr('django.static_root', PUBLIC_ROOT.child('static'))
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    BASE_DIR.child('static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)

MEDIA_ROOT = CONFIG.getstr('django.media_root', PUBLIC_ROOT.child('media'))
MEDIA_URL = '/media/'

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

PIPELINE_CSS = {
    'base': {
        'source_filenames': (
            'css/bootstrap.css',
            'css/project.css',
        ),
        'output_filename': 'css/base.css',
    },
}

PIPELINE_JS = {
    'base': {
        'source_filenames': (
            'js/jquery.js',
            'js/jquery.lazy.js',
            'js/bootstrap.js',
        ),
        'output_filename': 'js/base.js',
    },
    'meme': {
        'source_filenames': (
            'js/meme.js',
        ),
        'output_filename': 'js/meme.js',
    },
}

PIPELINE_JS_COMPRESSOR = None

PIPELINE = {
    'STYLESHEETS': PIPELINE_CSS,
    'JAVASCRIPT': PIPELINE_JS,
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '[phase] %(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
        # Send info messages to syslog
        'syslog': {
            'level': 'INFO',
            'class': 'logging.handlers.SysLogHandler',
            'facility': SysLogHandler.LOG_LOCAL2,
            'address': '/dev/log' if os.path.exists('/dev/log') else '/var/run/syslog',
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'WARNING',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
        # critical errors are logged to sentry
        #'sentry': {
        #    'level': 'ERROR',
        #    'filters': ['require_debug_false'],
        #    'class': 'raven.contrib.django.handlers.SentryHandler',
        #},
    },
    'loggers': {
        # This is the "catch all" logger
        '': {
            'handlers': ['console', 'syslog', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

LOGIN_REDIRECT_URL = reverse_lazy('image_list')

if ENVIRONMENT == 'prod':
    DEFAULT_FROM_EMAIL = CONFIG.getstr('email.from')
    EMAIL_HOST = CONFIG.getstr('email.host', "localhost")
    EMAIL_PORT = CONFIG.getint('email.port', 25)

    SECURE_PROXY_SSL_HEADER = ('HTTP_X_REAL_SCHEME', 'https')
    SESSION_COOKIE_NAME = 's'
    SESSION_COOKIE_SECURE = True

    TEMPLATES[0]['OPTIONS']['loaders'] = [
        ('django.template.loaders.cached.Loader', [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]), 
    ]

    INSTALLED_APPS += [
        'raven.contrib.django.raven_compat',
    ]
    RAVEN_CONFIG = {
        'dsn': CONFIG.getstr('raven.dsn')
    }

if ENVIRONMENT in ('dev', 'test'):
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    INSTALLED_APPS += (
        'debug_toolbar',
        'django_extensions',
    )

    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

LEGAL_MENTIONS = CONFIG.getstr('img.legal_mentions')
