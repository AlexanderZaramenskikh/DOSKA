import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project1.settings')

app = Celery('project1')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'simpleapp.tasks.send_week',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}

app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'simpleapp.tasks.new_post',
    },
}

app.autodiscover_tasks()