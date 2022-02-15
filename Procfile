release: python manage.py migrate
web: gunicorn groves.wsgi
worker: celery -A groves worker --beat --scheduler django --loglevel=info