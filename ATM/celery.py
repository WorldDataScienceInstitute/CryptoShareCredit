# from __future__ import absolute_import, unicode_literals
# import os
# import requests

# from celery import Celery
# from celery.schedules import crontab

# # set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ATM.settings')

# app = Celery('ATM')
# app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
#                 CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])
# # Using a string here means the worker doesn't have to serialize
# # the configuration object to child processes.
# # - namespace='CELERY' means all celery-related configuration keys
# #   should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings', namespace='CELERY')

# # Load task modules from all registered Django app configs.
# app.autodiscover_tasks()

# @app.on_after_finalize.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls daily routine every day at midnight
#     sender.add_periodic_task(crontab(minute=0, hour=0), DailyRoutine.s('DailyRoutine'), name='DailyRoutine')
#     sender.add_periodic_task(crontab(minute='*/1'), UpdateExchangeRates.s('UpdateExchangeRates'), name='UpdateExchangeRates')


# #Checks for expired addresses and loans
# @app.task
# def DailyRoutine(msg):

#     QUERYSTRING = {
#                 "key": "DailyCryptoshareRoutine"
#                 }
    
#     URL = "https://www.cryptoshareapp.com/atm/DailyRoutine/"
#     response = requests.get(url=URL, params=QUERYSTRING)

#     print(f"Executed: {msg} ")

# @app.task
# def UpdateExchangeRates(msg):
    
#     URL = "https://www.cryptoshareapp.com/atm/UpdateExchangeRates/"
#     response = requests.get(url=URL)

#     print(f"Executed: {msg} ")

# @app.task
# def add(x, y):
#     z = x + y
#     print(z)