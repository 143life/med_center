from django.db import models
from core.apps.common.models import TimedBaseModel
from .ticket import Ticket
from .specialization import Specialization


class Appointment(TimedBaseModel):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE)
    completed = models.BooleanField("Завершен", default=False)

    def __str__(self):
        return f"{self.ticket}, {self.specialization}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["ticket", "specialization"], name="unique_ticket_specialization"
            )
        ]
        verbose_name = "Приём"
        verbose_name_plural = "Приёмы"
