from django.db import models

from core.apps.common.models import TimedBaseModel
from core.apps.medcenter.entities import Ticket as TicketEntity

from .person import Person


class Ticket(TimedBaseModel):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    datetime = models.DateTimeField("Дата и время создания")
    number = models.IntegerField("Номер", max_length=3)
    completed = models.BooleanField("Завершен", default=False)

    def to_entity(self) -> TicketEntity:
        return TicketEntity(
            id=self.id,  # noqa
            person=self.person.to_entity(),
            datetime=self.datetime,
            number=self.number,
            completed=self.completed,
        )

    @staticmethod
    def from_entity(entity: TicketEntity) -> "Ticket":
        return Ticket(
            id=entity.id,
            person=Person.from_entity(entity.person),
            datetime=entity.datetime,
            number=entity.number,
            completed=entity.completed,
        )

    def __str__(self):
        return f"{self.number}"

    class Meta:
        verbose_name = "Талон"
        verbose_name_plural = "Талоны"
