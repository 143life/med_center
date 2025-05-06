from django.db import models

from core.apps.common.models import TimedBaseModel
from core.apps.medcenter.entities import Specialization as SpecializationEntity


class Specialization(TimedBaseModel):
    title = models.CharField("Название", max_length=25)

    def to_entity(self):
        return SpecializationEntity(
            title=self.title,
        )

    @staticmethod
    def from_entity(entity: SpecializationEntity) -> "Specialization":
        return Specialization(title=entity.title)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Специальность"
        verbose_name_plural = "Специальность"
