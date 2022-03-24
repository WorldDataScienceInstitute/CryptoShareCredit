"""
WSGI config for ATM project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""
from __future__ import absolute_import, unicode_literals
import os

from django.core.wsgi import get_wsgi_application

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from atm_functions.celery import app as celery_app

__all__ = ('celery_app',)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ATM.settings')

application = get_wsgi_application()
