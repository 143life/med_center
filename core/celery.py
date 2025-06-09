from celery import Celery


app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(["core.apps.medcenter"])

app.conf.enable_utc = False
app.conf.timezone = "Europe/Moscow"

app.conf.beat_schedule = {
    "auto-complete-tickets": {
        "task": "core.apps.medcenter.tasks.auto_complete_tickets",
        "schedule": 10.0,  # Каждые 10 секунд
    },
    "auto-complete-appointments": {
        "task": "core.apps.medcenter.tasks.auto_complete_appointments_and_delete_from_waiting_list",  # noqa
        "schedule": 5.0,  # Каждые 10 секунд
    },
    "auto-update-waiting-list": {
        "task": "core.apps.medcenter.tasks.auto_update_to_waiting_list",
        "schedule": 5.0,  # Каждые 5 секунд
    },
}
