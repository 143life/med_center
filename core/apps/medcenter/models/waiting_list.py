from django.db import models

from core.apps.common.models import TimedBaseModel

from .doctor_schedule import DoctorSchedule
from .ticket import Ticket


class WaitingList(TimedBaseModel):
    ticket = models.OneToOneField(
        Ticket,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name="Талон",
    )
    # Ссылка на всю модель, но это поле нужно только для cabinet_number
    doctor_schedule = models.ForeignKey(
        DoctorSchedule,
        on_delete=models.CASCADE,
        verbose_name="Расписание врача",
    )
    time_begin = models.DateTimeField("Время начала приема")
    time_end = models.DateTimeField("Время окончания приема")

    def __str__(self):
        return f"Ожидание {self.ticket} - Кабинет {self.doctor_schedule.cabinet_number} ({self.time_begin.strftime('%H:%M')} - {self.time_end.strftime('%H:%M')})"  # noqa

    class Meta:
        verbose_name = "Очередь"
        verbose_name_plural = "Очередь"
        app_label = "medcenter"
        ordering = ["time_begin"]  # Сортировка по времени начала
