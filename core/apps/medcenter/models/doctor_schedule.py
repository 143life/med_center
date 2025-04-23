from django.db import models

from core.apps.common.models import TimedBaseModel

from .doctor import Doctor
from .schedule import Schedule


class DoctorSchedule(TimedBaseModel):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    cabinet_number = models.IntegerField("Кабинет", max_length=3)

    def __str__(self):
        return f"{self.doctor}, {self.schedule}, {self.cabinet_number}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "schedule", "cabinet_number"],
                name="unique_doctor_schedule_cabnumber",
            ),
        ]
        verbose_name = "Расписание работы"
        verbose_name_plural = "Расписания работы"
