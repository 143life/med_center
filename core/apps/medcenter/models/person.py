from django.db import models

from core.apps.common.models import TimedBaseModel
from core.apps.medcenter.entities import Person as PersonEntity


class Person(TimedBaseModel):
    """
    Just a view to write to the database
    """

    first_name = models.CharField("Имя", max_length=25)
    last_name = models.CharField("Фамилия", max_length=25)
    patronymic = models.CharField("Отчество", max_length=25)
    date_birth = models.DateField("Дата рождения")
    # noqa is_visible = models.BooleanField('Виден ли в списке', default=True)

    def to_entity(self) -> PersonEntity:
        """
        Method that create entity object (from ../entities/person.py)
        """
        return PersonEntity(
            id=self.id,  # id=self.pk
            first_name=self.first_name,
            last_name=self.last_name,
            patronymic=self.patronymic,
            date_birth=self.date_birth,
        )

    @staticmethod
    def from_entity(entity: PersonEntity) -> "Person":
        return Person(
            id=entity.id,  # id=self.pk
            first_name=entity.first_name,
            last_name=entity.last_name,
            patronymic=entity.patronymic,
            date_birth=entity.date_birth,
        )

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronymic} ({self.date_birth.strftime('%d.%m.%Y')})"  # noqa

    class Meta:
        verbose_name = "Человек"
        verbose_name_plural = "Люди"
        ordering = ["last_name", "first_name", "patronymic"]
        app_label = "medcenter"
