from django.db import models

from core.apps.common.models import TimedBaseModel
from core.apps.medcenter.entities import Specialization as SpecializationEntity


class Specialization(TimedBaseModel):
    title = models.CharField("Название специальности", max_length=25)

    def to_entity(self):
        return SpecializationEntity(
            id=self.id,
            title=self.title,
        )

    @staticmethod
    def from_entity(entity: SpecializationEntity) -> "Specialization":
        return Specialization(id=entity.id, title=entity.title)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Специальность"
        verbose_name_plural = "Специальности"
        app_label = "medcenter"
        ordering = ["title"]
