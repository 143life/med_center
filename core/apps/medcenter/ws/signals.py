# signals.py
from django.apps import apps
from django.db.models.signals import (
    post_delete,
    post_save,
)
from django.dispatch import receiver
from django.utils import timezone

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


@receiver([post_save, post_delete])
def send_queue_update(sender, instance, **kwargs):
    # Проверяем, что сигнал от нужной модели
    if sender._meta.label != "medcenter.WaitingList":
        return
    channel_layer = get_channel_layer()
    WaitingList = apps.get_model("medcenter", "WaitingList")
    now = timezone.now()
    queue = (
        WaitingList.objects.filter()
        .select_related(
            "ticket",
            "doctor_schedule",
        )
        .order_by("time_begin")
    )  # Сортируем по времени начала приема
    serialized_queue = [
        {
            "ticket__number": item.ticket.number,
            "doctor_schedule__cabinet_number": item.doctor_schedule.cabinet_number,  # noqa
            "time_begin": item.time_begin.isoformat(),
            "time_end": item.time_end.isoformat(),
            "status": (
                "current"
                if item.time_begin <= now <= item.time_end
                else "waiting"
            ),
        }
        for item in queue
    ]

    async_to_sync(channel_layer.group_send)(
        "queue_updates",
        {"type": "queue.update", "queue": serialized_queue},
    )
