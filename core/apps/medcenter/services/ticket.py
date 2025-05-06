from django.db import transaction
from django.db.models import Q

from core.api.v1.medcenter.filters import TicketFilters
from core.apps.medcenter.entities import Ticket
from core.apps.medcenter.entities.appointment import Appointment
from core.apps.medcenter.models import Ticket as TicketDTO
from core.apps.medcenter.models.person import Person as PersonDTO
from core.apps.medcenter.services.appointment import ORMAppointmentService
from core.apps.medcenter.services.base import BaseService


class ORMTicketService(BaseService[TicketFilters, Ticket, TicketDTO]):
    filters = TicketFilters
    entity = Ticket
    model = TicketDTO

    @classmethod
    def _build_query(cls, filters: TicketFilters) -> Q:
        query = Q()

        return query

    @classmethod
    @transaction.atomic
    def create_ticket_with_appointments(
        cls,
        ticket: Ticket,
        appointment_list: list[dict],
    ) -> tuple[Ticket, list[Appointment]]:
        """Создает талон и приемы в одной транзакции"""
        ticket_dto = TicketDTO.objects.create(
            person=PersonDTO.from_entity(ticket.person),
            datetime=ticket.datetime,
            number=ticket.number,
            completed=ticket.completed,
        )
        ticket_entity = ticket_dto.to_entity()
        appointment_list_response = [
            ORMAppointmentService.create_appointment(
                ticket=ticket_entity,
                specialization_id=item["specialization_id"],
                completed=item["completed"],
            )
            for item in appointment_list
        ]

        return (ticket_entity, appointment_list_response)
