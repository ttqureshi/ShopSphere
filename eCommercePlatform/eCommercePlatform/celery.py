from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eCommercePlatform.settings")

app = Celery("eCommercePlatform")
app.conf.enable_utc = False

app.conf.update(timezone="Asia/Karachi")

app.config_from_object(settings, namespace="CELERY")

app.autodiscover_tasks(
    lambda: settings.INSTALLED_APPS
)  # automatically discover tasks from all Django apps that are registered in INSTALLED_APPS


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
