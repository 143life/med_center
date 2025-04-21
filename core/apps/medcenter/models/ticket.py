from django.db import models
from core.apps.common.models import TimedBaseModel
from .person import Person


class Ticket(TimedBaseModel):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    datetime = models.DateTimeField("Дата и время создания")
    number = models.IntegerField("Номер", max_length=3)
    completed = models.BooleanField("Завершен", default=False)

    def __str__(self):
        return f"{self.number}"

    class Meta:
        verbose_name = "Талон"
        verbose_name_plural = "Талоны"
