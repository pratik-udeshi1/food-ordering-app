from __future__ import absolute_import, unicode_literals
import os
import logging
from celery import Celery
from celery.signals import setup_logging

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant.settings')
# os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
# Get the base REDIS URL, default to redis' default
BASE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')


# create a Celery instance and configure it using the settings from Django.
celery_app = Celery('restaurant')

# load task modules from all registered Django app configs.
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# auto-discover tasks in all installed apps
celery_app.autodiscover_tasks()

celery_app.conf.broker_url = BASE_REDIS_URL

# this allows you to schedule items in the Django admin.
celery_app.conf.beat_scheduler = 'django_celery_beat.schedulers.DatabaseScheduler'


# Configure Celery logging to a file
@setup_logging.connect
def configure_logging(sender=None, **kwargs):
    logging.getLogger('celery').setLevel(logging.DEBUG)
    file_handler = logging.FileHandler('celery_debug.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logging.getLogger('celery').addHandler(file_handler)
