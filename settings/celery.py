from celery import Celery
from django.conf import settings
import os
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.main')
app = Celery('settings')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

CELERY_TIMEZONE = 'Asia/Kolkata'
BROKER_URL = os.environ.get('BROKER_URL', "redis://localhost:6379")
DJANGO_CELERY_BEAT_TZ_AWARE = True


CELERY_QUEUES_DICT = {
    "fampay-queue-v1": "fampay-queue-v1"
}

app.conf.beat_schedule = {
    "sync-latest-yt-video": {
        "task": "youtube.tasks.sync_latest_yt_video",
        "schedule": 60,  # run after every 60 sec
        'options': {'queue': CELERY_QUEUES_DICT.get("fampay-queue-v1")}
    }

}
