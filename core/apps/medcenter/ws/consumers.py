import json

from django.apps import apps

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
        queue = WaitingList.objects.filter().select_related(
            "ticket",
            "doctor_schedule",
        )

        return [
            {
                "ticket__number": item.ticket.number,
                "doctor_schedule__cabinet_number": item.doctor_schedule.cabinet_number,  # noqa
                "time_begin": item.time_begin.isoformat(),
                "time_end": item.time_end.isoformat(),
            }
            for item in queue
        ]

    async def send_current_queue(self):
        queue = await self.get_current_queue()
        await self.send(
            text_data=json.dumps({"type": "queue_update", "queue": queue}),
        )

    async def queue_update(self, event):
        await self.send(text_data=json.dumps(event))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.queue_group,
            self.channel_name,
        )
