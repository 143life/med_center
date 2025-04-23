from django.db import models

from core.apps.common.models import TimedBaseModel

from .doctor import Doctor


class Schedule(TimedBaseModel):
    datetime_begin = models.DateTimeField("Дата начала")
    datetime_end = models.DateTimeField("Дата окончания")
    monday = models.BooleanField("Понедельник", default=False)
    tuesday = models.BooleanField("Вторник", default=False)
    wednesday = models.BooleanField("Среда", default=False)
    thursday = models.BooleanField("Четверг", default=False)
    friday = models.BooleanField("Пятница", default=False)
    saturday = models.BooleanField("Суббота", default=False)
    sunday = models.BooleanField("Воскресенье", default=False)

    doctors = models.ManyToManyField(Doctor, through="DoctorSchedule")

    def __str__(self):
        return f"С {self.datetime_begin} по {self.datetime_end}"

    class Meta:
        verbose_name = "Расписание"
        verbose_name_plural = "Расписания"
