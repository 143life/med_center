from django.http import HttpRequest
from ninja import Query, Router

from core.api.filters import PaginationIn, PaginationOut
from core.api.schemas import ApiResponse, ListPaginatedResponse
from core.api.v1.medcenter.filters import PersonFilters
from core.apps.medcenter.services.person import BasePersonService, ORMPersonService
from .schemas.person import PersonSchema

router = Router(tags=["medcenter"])


@router.get("/person", response=ApiResponse[ListPaginatedResponse[PersonSchema]])
def get_person_list_handler(
    request: HttpRequest,
    filters: Query[PersonFilters],
    pagination_in: Query[PaginationIn],
) -> ApiResponse[ListPaginatedResponse[PersonSchema]]:
    service: BasePersonService = ORMPersonService()
    person_list = service.get_person_list(filters=filters, pagination=pagination_in)
    person_count = service.get_person_count(filters=filters)
    items = [PersonSchema.from_entity(obj) for obj in person_list]
    pagination_out = PaginationOut(
        offset=pagination_in.offset, limit=pagination_in.limit, total=person_count
    )

    return ApiResponse(
        data=ListPaginatedResponse(items=items, pagination=pagination_out)
    )
