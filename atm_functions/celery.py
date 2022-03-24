from __future__ import absolute_import, unicode_literals

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

    url = "https://5e48-185-153-177-98.ngrok.io/atm/TestReceiver/"
    data = {}

    request2 = requests.post(url, json=data)
    return('Request: {0!r}'.format(self.request))