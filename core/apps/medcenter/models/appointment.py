from django.db import models

from core.apps.common.models import TimedBaseModel
from core.apps.medcenter.entities import Appointment as AppointmentEntity

from .specialization import Specialization
from .ticket import Ticket


class Appointment(TimedBaseModel):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        verbose_name="Талон",
    )
    specialization = models.ForeignKey(
        Specialization,
        on_delete=models.CASCADE,
        verbose_name="Специальность",
    )
    completed = models.BooleanField("Завершен", default=False)

    def to_entity(self) -> AppointmentEntity:
        return AppointmentEntity(
            ticket=self.ticket.to_entity(),
            specialization=self.specialization.to_entity(),
            completed=self.completed,
        )

    @staticmethod
    def from_entity(entity: AppointmentEntity) -> "Appointment":
        return Appointment(
            ticket=Ticket.from_entity(entity.ticket),
            specialization=Specialization.from_entity(entity.specialization),
            completed=entity.completed,
        )

    def __str__(self):
        status = "Завершен" if self.completed else "В ожидании"
        return f"Приём {self.ticket} - {self.specialization} ({status})"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["ticket", "specialization"],
                name="unique_ticket_specialization",
            ),
        ]
        verbose_name = "Приём"
        verbose_name_plural = "Приёмы"
        app_label = "medcenter"
        ordering = ["-created_at"]  # Сортировка по умолчанию
