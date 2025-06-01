from django.db.models import Q

from core.api.v1.medcenter.filters import AppointmentFilters
from core.apps.medcenter.entities.appointment import Appointment
from core.apps.medcenter.entities.ticket import Ticket
from core.apps.medcenter.models.appointment import (
    Appointment as AppointmentDTO,
)
from core.apps.medcenter.models.specialization import (
    Specialization as SpecializationDTO,
)
from core.apps.medcenter.models.ticket import Ticket as TicketDTO
from core.apps.medcenter.services.base import BaseService


class ORMAppointmentService(
    BaseService[AppointmentFilters, Appointment, AppointmentDTO],
):
    filters = AppointmentFilters
    model = AppointmentDTO
    entity = Appointment

    @classmethod
    def _build_query(cls, filters: AppointmentFilters) -> Q:
        query = Q()

        return query

    @classmethod
    def create_appointment(
        cls,
        ticket: Ticket,
        specialization_id: int,
        completed: bool,
    ) -> Appointment:
        appointment_dto = AppointmentDTO.objects.create(
            ticket=TicketDTO.from_entity(ticket),
            specialization=SpecializationDTO.objects.get(id=specialization_id),
            completed=completed,
        )

        return appointment_dto.to_entity()
