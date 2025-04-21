from django.db import models
from core.apps.common.models import TimedBaseModel
from .person import Person
from .specialization import Specialization


class Doctor(TimedBaseModel):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, primary_key=True)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.person}, {self.specialization}"

    class Meta:
        verbose_name = "Врач"
        verbose_name_plural = "Врачи"
