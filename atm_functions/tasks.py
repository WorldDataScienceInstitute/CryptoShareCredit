from celery import Celery, shared_task
from celery.schedules import crontab
import os
from atm_functions.models import Cryptocurrency

app = Celery('ATM')

app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
                CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

@app.on_after_configure.connect
def daily_test_task(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(30.0, task_test.s('THIS IS A TEST EVERY 30 SECS'), name='add every 30')

@app.task
def task_test(arg):
    print(arg)


@app.task
def test():
    counter = Cryptocurrency.objects.all().count()
    c = Cryptocurrency(currency_name=f"Test{counter}", contract=f"0x0_{counter}", wallet_address="0x0", blockchain="0x0", network="0x0", symbol="0x0")
    c.save()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))