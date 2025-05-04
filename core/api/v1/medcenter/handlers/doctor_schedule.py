from django.http import HttpRequest
from ninja import Query, Router
from core.api.filters import PaginationIn
from core.api.schemas import ApiResponse, ListPaginatedResponse
from core.api.v1.medcenter.filters import DoctorScheduleFilters
from core.api.v1.medcenter.handlers.base import BaseHandler
from core.api.v1.medcenter.schemas.doctor_schedule import DoctorScheduleSchema
from core.apps.medcenter.services.doctor_schedule import ORMDoctorScheduleService

router = Router(tags=[])

class DoctorScheduleHandler(BaseHandler[DoctorScheduleFilters, DoctorScheduleSchema, ORMDoctorScheduleService]):
	filters = DoctorScheduleFilters
	schema = DoctorScheduleSchema
	service = ORMDoctorScheduleService

	@router.get(
		"/list",
		response=ApiResponse[ListPaginatedResponse[DoctorScheduleSchema]]
	)
	def get_doctor_schedule_list_handler(
		request: HttpRequest,
		filters: Query[DoctorScheduleFilters],
		pagination_in: Query[PaginationIn]
	) -> ApiResponse[ListPaginatedResponse[DoctorScheduleSchema]]:
		return DoctorScheduleHandler.get_list_handler(
			request=request,
			filters=filters,
			pagination_in=pagination_in
		)