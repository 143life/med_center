from django.http import HttpRequest
from ninja import Query, Router
from core.api.filters import PaginationIn
from core.api.schemas import ApiResponse, ListPaginatedResponse
from core.api.v1.medcenter.filters import WaitingListFilters
from core.api.v1.medcenter.handlers.base import BaseHandler
from core.api.v1.medcenter.schemas.waiting_list import WaitingListSchema
from core.apps.medcenter.services.waiting_list import ORMWaitingListService

router = Router(tags=[])

class WaitingListHandler(BaseHandler[WaitingListFilters, WaitingListSchema, ORMWaitingListService]):
	filters = WaitingListFilters
	schema = WaitingListSchema
	service = ORMWaitingListService

	@router.get(
		"/list",
		response=ApiResponse[ListPaginatedResponse[WaitingListSchema]]
	)
	def get_waiting_list_list_handler(
		request: HttpRequest,
		filters: Query[WaitingListFilters],
		pagination_in: Query[PaginationIn]
	) -> ApiResponse[ListPaginatedResponse[WaitingListSchema]]:
		return WaitingListHandler.get_list_handler(
			request=request,
			filters=filters,
			pagination_in=pagination_in
		)