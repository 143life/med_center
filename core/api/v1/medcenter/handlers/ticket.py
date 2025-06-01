from django.http import HttpRequest

from ninja import (
    Query,
    Router,
)

from core.api.filters import PaginationIn
from core.api.schemas import (
    ApiResponse,
    ListPaginatedResponse,
)
from core.api.v1.medcenter.filters import TicketFilters
from core.api.v1.medcenter.handlers.base import BaseHandler
from core.api.v1.medcenter.schemas.appointment import AppointmentSchema
from core.api.v1.medcenter.schemas.request import TicketCreateRequest
from core.api.v1.medcenter.schemas.response import TicketOut
from core.api.v1.medcenter.schemas.ticket import TicketSchema
from core.apps.medcenter.services.ticket import ORMTicketService


router = Router(tags=[])


class TicketHandler(
    BaseHandler[TicketFilters, TicketSchema, ORMTicketService],
):
    filters = TicketFilters
    schema = TicketSchema
    service = ORMTicketService

    @router.get(
        "/list",
        response=ApiResponse[ListPaginatedResponse[TicketSchema]],
    )
    def get_ticket_list_handler(
        request: HttpRequest,
        filters: Query[TicketFilters],
        pagination_in: Query[PaginationIn],
    ) -> ApiResponse[ListPaginatedResponse[TicketSchema]]:
        return TicketHandler.get_list_handler(
            request=request,
            filters=filters,
            pagination_in=pagination_in,
        )

    @router.post("/create_with_appointments", response=ApiResponse[TicketOut])
    def create_ticket_handler(
        request: HttpRequest,
        payload: TicketCreateRequest,
    ) -> ApiResponse[TicketOut]:
        service = ORMTicketService
        ticket = TicketSchema.from_ticket_create_request(payload)
        ticket, appointments = service.create_ticket_with_appointments(
            ticket=TicketSchema.to_entity(ticket),
            appointment_list=payload.appointment_list,
        )

        appointment_out_list = [
            AppointmentSchema.from_entity(appointment).to_appointment_out()
            for appointment in appointments
        ]
        ticket_schema = TicketSchema.from_entity(ticket)

        ticket_out = TicketOut.from_ticket_and_appointment_out(
            ticket=ticket_schema,
            appointment_out_list=appointment_out_list,
        )

        return ApiResponse(data=ticket_out)
