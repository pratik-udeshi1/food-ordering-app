# celery_config.py

from __future__ import absolute_import, unicode_literals

import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant.settings')

# create a Celery instance and configure it using the settings from Django.
celery_app = Celery('restaurant')

# load task modules from all registered Django app configs.
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# auto-discover tasks in all installed apps
celery_app.autodiscover_tasks()

# This allows you to use the celery -A restaurant worker -l info command
celery = celery_app
