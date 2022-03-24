release: python manage.py migrate
web: gunicorn ATM.wsgi
worker: celery --app atm_functions worker