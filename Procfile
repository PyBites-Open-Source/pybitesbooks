release: python manage.py migrate
web: gunicorn myreadinglist.wsgi --log-file -
worker: celery -A myreadinglist worker --concurrency 1 -l info
