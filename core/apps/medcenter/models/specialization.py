from django.db import models
from core.apps.common.models import TimedBaseModel


class Specialization(TimedBaseModel):
    title = models.CharField("Название", max_length=25)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Специальность"
        verbose_name_plural = "Специальность"
