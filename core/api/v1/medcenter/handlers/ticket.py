from django.http import HttpRequest
from ninja import Query, Router
from core.api.filters import PaginationIn
from core.api.schemas import ApiResponse, ListPaginatedResponse
from core.api.v1.medcenter.filters import TicketFilters
from core.api.v1.medcenter.handlers.base import BaseHandler
from core.api.v1.medcenter.schemas.ticket import TicketSchema
from core.apps.medcenter.services.ticket import ORMTicketService

router = Router(tags=[])

class TicketHandler(BaseHandler[TicketFilters, TicketSchema, ORMTicketService]):
	filters = TicketFilters
	schema = TicketSchema
	service = ORMTicketService

	@router.get(
		"/list",
		response=ApiResponse[ListPaginatedResponse[TicketSchema]]
	)
	def get_ticket_list_handler(
		request: HttpRequest,
		filters: Query[TicketFilters],
		pagination_in: Query[PaginationIn]
	) -> ApiResponse[ListPaginatedResponse[TicketSchema]]:
		return TicketHandler.get_list_handler(
			request=request,
			filters=filters,
			pagination_in=pagination_in
		)