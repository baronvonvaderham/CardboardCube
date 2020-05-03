# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os
from CardboardCube import settings
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

app = Celery('CardboardCube', backend=settings.CELERY_RESULT_BACKEND)
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {self.request}')
