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
from core.api.v1.medcenter.filters import DoctorFilters
from core.api.v1.medcenter.handlers.base import BaseHandler
from core.api.v1.medcenter.schemas.doctor import DoctorSchema
from core.apps.medcenter.services.doctor import ORMDoctorService


router = Router(tags=[])


class DoctorHandler(
    BaseHandler[DoctorSchema, ORMDoctorService, DoctorFilters],
):
    schema = DoctorSchema
    service = ORMDoctorService
    filters = DoctorFilters

    @router.get(
        "/list",
        response=ApiResponse[ListPaginatedResponse[DoctorSchema]],
    )
    def get_doctor_list_handler(
        request: HttpRequest,
        filters: Query[DoctorFilters],
        pagination_in: Query[PaginationIn],
    ) -> ApiResponse[ListPaginatedResponse[DoctorSchema]]:
        return DoctorHandler.get_list_handler(
            request=request,
            filters=filters,
            pagination_in=pagination_in,
        )
