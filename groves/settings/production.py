import os
from .base import *

# Configure Django App for Heroku.
import django_heroku

django_heroku.settings(locals())

DEBUG = False


# Emails
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ["EMAIL_HOST"]
EMAIL_HOST_PASSWORD = os.environ["EMAIL_PASSWORD"]
