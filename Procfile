release: python manage.py migrate
web: gunicorn groves.wsgi
celery: celery -A groves worker -B