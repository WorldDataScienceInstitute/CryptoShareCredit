from __future__ import absolute_import, unicode_literals
import os
from django.conf import settings


from celery import Celery
from celery.schedules import crontab

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

@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 30 seconds.
    sender.add_periodic_task(30.0, test.s('THIS IS A TEST EVERY 30 SECS'), name='add every 30')
    # sender.add_periodic_task(
    #     crontab(minute=0, hour=0),
    #     test.s('Happy Day!'),
    # )
#




@app.task
def test(arg):
    print(arg)

@app.task
def add(x, y):
    z = x + y
    print(z)