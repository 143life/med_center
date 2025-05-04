from django.http import HttpRequest
from ninja import Query, Router

from core.api.filters import PaginationIn
from core.api.schemas import ApiResponse, ListPaginatedResponse
from core.api.v1.medcenter.filters import PersonFilters
from core.api.v1.medcenter.handlers.base import BaseHandler
from core.api.v1.medcenter.schemas.person import PersonSchema
from core.apps.medcenter.services.person import ORMPersonService

router = Router(tags=[])


class PersonHandler(BaseHandler[PersonSchema, PersonFilters, ORMPersonService]):
    schema = PersonSchema
    filters = PersonFilters
    service = ORMPersonService

    @router.get("/list", response=ApiResponse[ListPaginatedResponse[PersonSchema]])
    def get_person_list_handler(
        request: HttpRequest, filters: Query[PersonFilters], pagination_in: Query[PaginationIn]
    ) -> ApiResponse[ListPaginatedResponse[PersonSchema]]:
        return PersonHandler.get_list_handler(
            request=request, filters=filters, pagination_in=pagination_in
        )
