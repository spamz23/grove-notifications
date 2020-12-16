from GroveTasks.grove.tasks import pay_the_rent
import os

from celery import Celery
from celery.schedules import crontab
import redis


# Fetch the Redis connection string from the env, or use localhost by default
REDIS_URL = os.environ.get("REDISTOGO_URL", "redis://localhost")


redis_sv = redis.Redis.from_url(REDIS_URL, db=0)

# Setup the celery instance under the 'tasks' namespace
app = Celery("tasks")

# Use Redis as our broker and define json as the default serializer
app.conf.update(
    timezone="Europe/Lisbon",
    broker_url=REDIS_URL,
    task_serializer="json",
    accept_content=["json"],
    beat_schedule={
        "cleaning": {
            "task": "grove.tasks.cleaning",
            "schedule": crontab(hour=19, minute=0, day_of_week=0),
        },
        "tuition-fees": {
            "task": "grove.tasks.warn_tuition_fees",
            "schedule": crontab(0, 0, day_of_month=28),
        },
        "light": {
            "task": "grove.tasks.send_light_mileage",
            "schedule": crontab(0, 0, day_of_month=26),
        },
        "internet": {
            "task": "grove.tasks.send_internet_money",
            "schedule": crontab(0, 0, day_of_month=26),
        },
        "test": {
            "task": "grove.tasks.test",
            "schedule": crontab(minute=40, hour=0),
        },
        "cleaning-lady": {
            "task": "grove.tasks.cleaning_lady",
            "schedule": crontab(hour=19, minute=30, day_of_week=3),
        },
        "pay_the_rent": {
            "task": "grove.tasks.pay_the_rent",
            "schedule": crontab(hour=16, minute=30, day_of_month=7)
        }
    },
)
app.autodiscover_tasks(["grove"], force=True)
