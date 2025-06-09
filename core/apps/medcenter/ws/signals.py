# signals.py
from django.db.models.signals import (
    post_delete,
    post_save,
)
from django.dispatch import receiver

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


@receiver([post_save, post_delete], sender="medcenter.WaitingList")
def send_queue_update_trigger(sender, instance, **kwargs):
    """
    Отправляет простой сигнал-триггер в группу каналов,
    чтобы уведомить consumer'ы о необходимости обновить очередь.
    Сами данные здесь не отправляются, чтобы избежать дублирования логики.
    """
    channel_layer = get_channel_layer()
    if channel_layer:
        async_to_sync(channel_layer.group_send)(
            "queue_updates",
            {
                "type": "queue.update",  # Имя метода в consumer
            },
        )
