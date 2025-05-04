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
from core.api.v1.medcenter.filters import ScheduleFilters
from core.api.v1.medcenter.handlers.base import BaseHandler
from core.api.v1.medcenter.schemas.schedule import ScheduleSchema
from core.apps.medcenter.services.schedule import ORMScheduleService


router = Router(tags=[])


class ScheduleHandler(
    BaseHandler[ScheduleFilters, ScheduleSchema, ORMScheduleService],
):
    filters = ScheduleFilters
    schema = ScheduleSchema
    service = ORMScheduleService

    @router.get(
        "/list",
        response=ApiResponse[ListPaginatedResponse[ScheduleSchema]],
    )
    def get_schedule_list_handler(
        request: HttpRequest,
        filters: Query[ScheduleFilters],
        pagination_in: Query[PaginationIn],
    ) -> ApiResponse[ListPaginatedResponse[ScheduleSchema]]:
        return ScheduleHandler.get_list_handler(
            request=request,
            filters=filters,
            pagination_in=pagination_in,
        )
