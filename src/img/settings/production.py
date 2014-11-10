from base import *  # noqa
from django.core.exceptions import ImproperlyConfigured

try:
    import prod_private
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

DATABASES = get_prod_setting('DATABASES')

SECRET_KEY = get_prod_setting('SECRET_KEY')

ALLOWED_HOSTS = get_prod_setting('ALLOWED_HOSTS')

TIME_ZONE = get_prod_setting('TIME_ZONE')

STATIC_ROOT = get_prod_setting('STATIC_ROOT')

MEDIA_ROOT = get_prod_setting('MEDIA_ROOT')

RAVEN_CONFIG = get_prod_setting('RAVEN_CONFIG')
