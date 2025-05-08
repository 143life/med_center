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
from core.api.v1.medcenter.filters import SpecializationFilters
from core.api.v1.medcenter.handlers.base import BaseHandler
from core.api.v1.medcenter.schemas.specialization import SpecializationSchema
from core.apps.medcenter.services.specialization import (
    ORMSpecializationService,
)


router = Router(tags=[])


class SpecializationHandler(
    BaseHandler[
        SpecializationFilters,
        SpecializationSchema,
        ORMSpecializationService,
    ],
):
    filters = SpecializationFilters
    schema = SpecializationSchema
    service = ORMSpecializationService

    @router.get(
        "/list",
        response=ApiResponse[ListPaginatedResponse[SpecializationSchema]],
    )
    def get_specialization_list_handler(
        request: HttpRequest,
        filters: Query[SpecializationFilters],
        pagination_in: Query[PaginationIn],
    ) -> ApiResponse[ListPaginatedResponse[SpecializationSchema]]:
        return SpecializationHandler.get_list_handler(
            request=request,
            filters=filters,
            pagination_in=pagination_in,
        )

    @router.get("/all", response=ApiResponse[list[SpecializationSchema]])
    def get_specialization_all_handler(request: HttpRequest):
        return ApiResponse(
            data=[
                SpecializationSchema.from_entity(obj)
                for obj in ORMSpecializationService.get_specialization_list()
            ],
        )
