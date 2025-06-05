from django.db import models

from core.apps.common.models import TimedBaseModel
from core.apps.medcenter.entities import Doctor as DoctorEntity

from .person import Person
from .specialization import Specialization


class Doctor(TimedBaseModel):
    person = models.OneToOneField(
        Person,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name="Персональные данные",
    )
    specialization = models.ForeignKey(
        Specialization,
        on_delete=models.CASCADE,
        verbose_name="Специальность",
    )

    def to_entity(self):
        return DoctorEntity(
            person=self.person,
            specialization=self.specialization,
        )

    def __str__(self):
        return f"{self.person} - {self.specialization}"

    class Meta:
        verbose_name = "Врач"
        verbose_name_plural = "Врачи"
        app_label = "medcenter"
        ordering = ["person__last_name", "person__first_name"]
