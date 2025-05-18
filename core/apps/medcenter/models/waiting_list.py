from django.db import models

from core.apps.common.models import TimedBaseModel

from .doctor_schedule import DoctorSchedule
from .ticket import Ticket


class WaitingList(TimedBaseModel):
    ticket = models.OneToOneField(
        Ticket,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    # Ссылка на всю модель, но это поле нужно только для cabinet_number
    doctor_schedule = models.ForeignKey(
        DoctorSchedule,
        on_delete=models.CASCADE,
    )
    time_begin = models.DateTimeField("Время начала")
    time_end = models.DateTimeField("Время окончания")

    def __str__(self):
        return f"{self.ticket}, {self.time_begin}, {self.time_end}"

    class Meta:
        verbose_name = "Очередь"
        verbose_name_plural = "Очередь"
        app_label = "medcenter"
