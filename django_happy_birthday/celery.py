from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_happy_birthday.settings')

app = Celery('django_happy_birthday')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

