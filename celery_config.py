from celery import Celery
from decouple import config
# from settings import REDIS_URL
from celery.schedules import crontab




# Initialize Celery app
celery_app = Celery(
    "tasks",
    broker=config("REDIS_URL"),
    backend=config("REDIS_URL"),
)
celery_app = Celery(__name__)
celery_app.conf.broker_url = config('REDIS_URL')
celery_app.conf.result_backend =config('REDIS_URL') 
# Load Celery configuration
# celery_app.config_from_object("celery_config")
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# Start the Celery beat scheduler
celery_app.conf.beat_scheduler = "django_celery_beat.schedulers:DatabaseScheduler"
celery_app.conf.timezone = "UTC"
celery_app.broker_connection_retry_on_startup = True

# Add task routes  
celery_app.autodiscover_tasks(["tasks"])



celery_app.conf.beat_schedule = {
    "run-every-day-6am": {
        "task": "tasks.send_balance_alert",  # Task function
        "schedule": crontab(hour=6, minute=0),  # Run at 6 am every day
    },
    "run-every-day-1130pm": {
        "task": "tasks.send_balance_alert",  # Task function
        "schedule": crontab(hour=23, minute=30),  # Run at 11:30 pm every day
    },
}
