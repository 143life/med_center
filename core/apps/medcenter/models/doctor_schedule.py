from django.db import models

from core.apps.common.models import TimedBaseModel

from .doctor import Doctor
from .schedule import Schedule


class DoctorSchedule(TimedBaseModel):
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        verbose_name="Врач",
    )
    schedule = models.ForeignKey(
        Schedule,
        on_delete=models.CASCADE,
        verbose_name="Расписание",
    )
    cabinet_number = models.IntegerField("Номер кабинета")

    def __str__(self):
        return (
            f"{self.doctor} - Кабинет {self.cabinet_number} ({self.schedule})"
        )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "schedule", "cabinet_number"],
                name="unique_doctor_schedule_cabnumber",
            ),
        ]
        verbose_name = "Расписание работы"
        verbose_name_plural = "Расписания работы"
        app_label = "medcenter"
        ordering = ["doctor", "schedule__datetime_begin"]
