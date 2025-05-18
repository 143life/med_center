import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.project.settings.local")

app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(["core.apps.medcenter"])

app.conf.beat_schedule = {
    "check-expired-appointments-every-10-seconds": {
        "task": "core.apps.medcenter.tasks."
        + "auto_complete_appointments_and_delete_from_waiting_list",
        "schedule": 10.0,  # Каждые 10 секунд
    },
    "filling-the-queue": {
        "task": "core.apps.medcenter.tasks.auto_update_to_waiting_list",
        "schedule": 5.0,  # каждые 5 секунд
    },
}
