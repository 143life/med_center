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
from core.api.v1.medcenter.filters import AppointmentFilters
from core.api.v1.medcenter.handlers.base import BaseHandler
from core.api.v1.medcenter.schemas.appointment import AppointmentSchema
from core.apps.medcenter.services.appointment import ORMAppointmentService


router = Router(tags=[])


class AppointmentHandler(
    BaseHandler[AppointmentFilters, AppointmentSchema, ORMAppointmentService],
):
    filters = AppointmentFilters
    schema = AppointmentSchema
    service = ORMAppointmentService

    @router.get(
        "/list",
        response=ApiResponse[ListPaginatedResponse[AppointmentSchema]],
    )
    def get_appointment_list_handler(
        request: HttpRequest,
        filters: Query[AppointmentFilters],
        pagination_in: Query[PaginationIn],
    ) -> ApiResponse[ListPaginatedResponse[AppointmentSchema]]:
        return AppointmentHandler.get_list_handler(
            request=request,
            filters=filters,
            pagination_in=pagination_in,
        )
