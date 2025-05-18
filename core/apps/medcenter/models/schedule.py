from django.db import models

from core.apps.common.models import TimedBaseModel
from core.apps.medcenter.entities.schedule import Schedule as ScheduleEntity

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

    def to_entity(self) -> ScheduleEntity:
        return ScheduleEntity(
            id=self.id,  # noqa
            datetime_begin=self.datetime_begin,
            datetime_end=self.datetime_end,
            monday=self.monday,
            tuesday=self.tuesday,
            wednesday=self.wednesday,
            thursday=self.thursday,
            friday=self.friday,
            saturday=self.saturday,
            sunday=self.sunday,
        )

    def __str__(self):
        return f"С {self.datetime_begin} по {self.datetime_end}"

    class Meta:
        verbose_name = "Расписание"
        verbose_name_plural = "Расписания"
        app_label = "medcenter"
