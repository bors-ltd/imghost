from .base import *  # noqa
from django.core.exceptions import ImproperlyConfigured

try:
    from . import prod_private
except ImportError:
    raise ImproperlyConfigured("Create a prod_private.py file in settings")


def get_prod_setting(setting):
    """Get the setting or return exception """
    try:
        return getattr(prod_private, setting)
    except AttributeError:
        error_msg = "The %s setting is missing from prod settings" % setting
        raise ImproperlyConfigured(error_msg)


DEBUG = False

TEMPLATE_DEBUG = False

INSTALLED_APPS += (
    'raven.contrib.django.raven_compat',
)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_REAL_SCHEME', 'https')

SESSION_COOKIE_NAME = 's'

SESSION_COOKIE_SECURE = True

DATABASES = get_prod_setting('DATABASES')

SECRET_KEY = get_prod_setting('SECRET_KEY')

ALLOWED_HOSTS = get_prod_setting('ALLOWED_HOSTS')

TIME_ZONE = get_prod_setting('TIME_ZONE')

STATIC_ROOT = get_prod_setting('STATIC_ROOT')

MEDIA_ROOT = get_prod_setting('MEDIA_ROOT')

RAVEN_CONFIG = get_prod_setting('RAVEN_CONFIG')

LEGAL_MENTIONS = get_prod_setting('LEGAL_MENTIONS')
