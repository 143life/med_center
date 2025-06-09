import json

from django.apps import apps
from django.utils import timezone

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


class QueueConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.queue_group = "queue_updates"
        await self.channel_layer.group_add(self.queue_group, self.channel_name)
        await self.accept()
        await self.send_current_queue()

    @database_sync_to_async
    def get_current_queue(self):
        WaitingList = apps.get_model("medcenter", "WaitingList")
        now = timezone.now()

        # 1. Запрашиваем из БД ТОЛЬКО АКТУАЛЬНЫЕ записи (еще не закончились)
        # Это решает проблему "пропадания" приемов.
        queue_from_db = (
            WaitingList.objects.filter(time_end__gt=now)
            .select_related(
                "ticket",
                "doctor_schedule__doctor__specialization",
            )
            .order_by("time_begin")
        )

        # 2. Вычисляем статус в Python, как и в вашем оригинальном коде.
        queue_data = [
            {
                "ticket_id": item.ticket.id,
                "ticket__number": item.ticket.number,
                "doctor_schedule__cabinet_number": item.doctor_schedule.cabinet_number,  # noqa
                "specialization__title": item.doctor_schedule.doctor.specialization.title,  # noqa
                "time_begin": item.time_begin.isoformat(),
                "time_end": item.time_end.isoformat(),
                "status": (
                    "current"
                    if item.time_begin <= now <= item.time_end
                    else "waiting"
                ),
            }
            for item in queue_from_db
        ]

        # 3. Сортируем готовый список в Python: сначала "current"
        # Это решает проблему с порядком отображения.
        queue_data.sort(
            key=lambda x: (x["status"] != "current", x["time_begin"]),
        )

        return queue_data

    async def send_current_queue(self):
        queue = await self.get_current_queue()
        await self.send(
            text_data=json.dumps({"type": "queue_update", "queue": queue}),
        )

    async def queue_update(self, event):
        # Вместо того чтобы доверять данным в event,
        # мы просто используем его как триггер для пересчета очереди.
        # Это гарантирует, что все клиенты получат одинаковые,
        # правильно отсортированные данные.
        await self.send_current_queue()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.queue_group,
            self.channel_name,
        )
