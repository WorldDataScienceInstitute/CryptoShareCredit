from __future__ import absolute_import, unicode_literals
import os


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
app.autodiscover_tasks()

@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 30 seconds.
    sender.add_periodic_task(crontab(minute="*/1"), test.s('DailyRoutine'), name='DailyRoutine')
    # sender.add_periodic_task(
    #     crontab(minute=0, hour=0),
    #     test.s('Happy Day!'),
    # )
#




@app.task
def test(msg):
    import requests

    QUERYSTRING = {
                "checksum": "482f9e2ed75e9df2fbd2753d17a0285460abea29840302ab10619efeff66fcba",
                "key": "DailyCryptoshareRoutine"
                }
    
    URL = "https://www.cryptoshareapp.com/atm/TestReceiver/"
    response = requests.get(url=URL, params=QUERYSTRING).json()

    print(f"Executed: {msg}")
    print(response)


@app.task
def add(x, y):
    z = x + y
    print(z)