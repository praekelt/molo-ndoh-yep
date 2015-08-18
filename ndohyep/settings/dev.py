from .base import *


DEBUG = True
TEMPLATE_DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_SUBJECT_PREFIX = '[b-wise.qa] '
WAGTAILADMIN_NOTIFICATION_FROM_EMAIL = 'no-reply@qa.b-wise.mobi'


try:
    from .local import *
except ImportError:
    pass
