import os
from sys import path
from os.path import basename
from django.core.urlresolvers import reverse_lazy
from unipath import Path
from logging.handlers import SysLogHandler


DJANGO_ROOT = Path(__file__).ancestor(3)
PROJECT_ROOT = DJANGO_ROOT.ancestor(1)
SITE_NAME = basename(PROJECT_ROOT)
CONFIGURATION_APP_ROOT = Path(__file__).ancestor(2)
PUBLIC_ROOT = PROJECT_ROOT.child('public')
path.append(DJANGO_ROOT)
path.append(CONFIGURATION_APP_ROOT)

SECRET_KEY = '7dcckq$8m2)mzwgu6&u#7+g4(3u#dl4k%9m9afpw+p-4!!!+ar'

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


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
    'south',
)

LOCAL_APPS = (
    'images',
    'memes',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE_CLASSES = (
    'pipeline.middleware.MinifyHTMLMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'img.middleware.CurrentSiteMiddleware',
)

ROOT_URLCONF = 'img.urls'

WSGI_APPLICATION = 'img.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'img.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = PUBLIC_ROOT.child('static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    DJANGO_ROOT.child('static'),
)

MEDIA_ROOT = PUBLIC_ROOT.child('media')
MEDIA_URL = '/media/'

TEMPLATE_DIRS = (
    DJANGO_ROOT.child('templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

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
        # We have to redefine this. See
        # http://stackoverflow.com/questions/20282521/django-request-logger-not-propagated-to-root
        'django.request': {
            'propagate': True,
        },
    }
}

LOGIN_REDIRECT_URL = reverse_lazy('image_list')
