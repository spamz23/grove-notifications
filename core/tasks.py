"""
Async tasks
"""
from django.contrib.auth import get_user_model
from celery import shared_task
from django_celery_beat.models import PeriodicTask


@shared_task
def notify(task_name, **kwargs):
    """
    Notifies users of weekly cleaning tasks.
    """
    task = PeriodicTask.objects.get(name=task_name)

    if "users" in kwargs:
        users = get_user_model().objects.filter(email__in=kwargs["users"])
    else:
        users = get_user_model().objects.all()

    for u in users:
        u.notify(task.name, task.description)
