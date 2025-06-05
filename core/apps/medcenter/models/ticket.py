from django.core.exceptions import ValidationError
from django.db import models

from core.apps.common.models import TimedBaseModel
from core.apps.medcenter.entities import Ticket as TicketEntity

from .person import Person


class Ticket(TimedBaseModel):
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        verbose_name="Пациент",
    )
    datetime = models.DateTimeField("Дата и время создания")
    number = models.IntegerField("Номер талона")
    completed = models.BooleanField("Завершен", default=False)

    def clean(self):
        # Проверяем, существует ли незавершенный талон с таким номером
        if not self.completed:
            existing_ticket = (
                Ticket.objects.filter(number=self.number, completed=False)
                .exclude(pk=self.pk)
                .first()
            )

            if existing_ticket:
                raise ValidationError(
                    {
                        "number": "Талон с таким номером есть и не завершен",
                    },
                )

    def save(self, *args, **kwargs):
        self.clean()  # Вызываем валидацию перед сохранением
        super().save(*args, **kwargs)

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
        return f"Талон №{self.number} - {self.person})"

    class Meta:
        verbose_name = "Талон"
        verbose_name_plural = "Талоны"
        app_label = "medcenter"
        ordering = ["-datetime"]  # Сортировка по умолчанию
        constraints = [
            models.UniqueConstraint(
                fields=["number"],
                condition=models.Q(completed=False),
                name="unique_uncompleted_ticket_number",
            ),
        ]
