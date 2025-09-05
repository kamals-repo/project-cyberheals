import os
from celery import Celery
from celery.schedules import crontab
from users.tasks import send_hourly_report


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(['tasks'])

app.conf.update(
    worker_pool='solo',
)

app.conf.beat_schedule = {
    'send-user-stats-every-hour': {
        'task': 'users.tasks.send_hourly_report.send_user_statistics_email',
        
        'schedule': crontab(minute=0),
    },
}