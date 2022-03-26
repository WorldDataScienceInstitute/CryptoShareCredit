release: python manage.py migrate
web: gunicorn ATM.wsgi
worker: celery --app ATM worker --loglevel=info --without-gossip --without-mingle --without-heartbeat -Ofair -B