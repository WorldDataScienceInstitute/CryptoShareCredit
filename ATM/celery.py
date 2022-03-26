from __future__ import absolute_import, unicode_literals
from django.conf import settings

import os

from celery import Celery

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
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)



@app.task
def test(arg):
    print(arg)

@app.task
def add(x, y):
    z = x + y
    print(z)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
