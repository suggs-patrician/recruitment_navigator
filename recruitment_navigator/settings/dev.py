from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-z)u7mbzm88v!rkrpqvk9=k%&doxea&p4=k4w*4t%2w1r$+ld@9"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

# CSRF settings
CSRF_TRUSTED_ORIGINS = [
    "https://work-1-qkpjoluleghnqdob.prod-runtime.all-hands.dev",
    "https://work-2-qkpjoluleghnqdob.prod-runtime.all-hands.dev",
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


try:
    from .local import *
except ImportError:
    pass
