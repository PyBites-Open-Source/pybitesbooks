release: python manage.py migrate
web: gunicorn myreadinglist.wsgi --log-file -
worker: celery -A myreadinglist worker -l info
