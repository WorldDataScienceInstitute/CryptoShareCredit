from __future__ import absolute_import, unicode_literals
from .models import User
from atm_functions.models import Account, Address, Balance, Cryptocurrency, TransactionA, TransactionB

import os

from celery import Celery
import requests

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ATM.settings')

app = Celery('ATM')
app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
                CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    # u = User.objects.get(pk=88)

    c_test = Cryptocurrency(currency_name="C_Test", contract="0x0", wallet_address="0x0", blockchain="0x0", network="0x0", symbol="0x0")
    c_test.save()
